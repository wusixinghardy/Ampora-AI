import os
import json
from typing import List, Dict, Any

# Import our modules
import src.services.lecture1 as lecture1
import src.services.visualization as visualization
import src.services.voice as voice

try:
    # In MoviePy v2, everything is exposed at the top level
    from moviepy import *
    
    # However, sometimes explicit imports help if the star import misses something
    if "ImageClip" not in globals():
        from moviepy.video.VideoClip import ImageClip
    if "AudioFileClip" not in globals():
        from moviepy.audio.io.AudioFileClip import AudioFileClip
    if "concatenate_videoclips" not in globals():
        from moviepy.video.compositing.concatenate import concatenate_videoclips
        
    MOVIEPY_AVAILABLE = True
    print(f"[Video] MoviePy v2.2.1 loaded successfully.")

except ImportError as e:
    print(f"⚠️ MoviePy Import Error: {e}")
    MOVIEPY_AVAILABLE = False


def generate_lecture_video(topic: str, output_filename: str = "lecture_video.mp4"):
    """
    Full pipeline to generate a video lecture from a topic string.
    Targeting MoviePy 2.2.1 syntax (.with_duration, .with_audio).
    """
    
    print(f"\n==================================================")
    print(f"🚀 STARTING VIDEO GENERATION FOR TOPIC: '{topic}'")
    print(f"==================================================\n")

    # ============================================================
    # PHASE 1: CONTENT GENERATION (LLM)
    # ============================================================
    print("--- [Phase 1] Generating Lecture Content ---")
    
    # 1.1 Objectives
    objectives = lecture1.generate_learning_objectives(topic)
    print(f"✅ Generated {len(objectives)} learning objectives.")
    
    # 1.2 Slide Plan
    plan = lecture1.generate_slide_plan(objectives)
    print(f"✅ Generated plan with {len(plan)} slides.")
    
    # 1.3 Full Slide Content (Script + Visual descriptions)
    slides_content = lecture1.generate_slide_content(plan)
    print(f"✅ Generated full content for {len(slides_content)} slides.")


    # ============================================================
    # PHASE 2: VISUALIZATION (IMAGE GEN)
    # ============================================================
    print("\n--- [Phase 2] Generating Slide Images ---")
    
    # Prepare data for visualization module
    slides_for_viz = []
    for s in slides_content:
        slides_for_viz.append({
            "title": s.get("title", "Untitled"),
            "bulletpoints": s.get("bulletpoints", []),
            "visual_step_description": s.get("visualization", "")
        })

    # Generate images
    image_paths = visualization.generate_visualizations_with_gemini(
        slide_steps=slides_for_viz,
        output_dir="output_visuals",
        model="gemini-3-pro-image-preview" 
    )
    
    if len(image_paths) != len(slides_content):
        print(f"⚠️ Warning: Requested {len(slides_content)} images but got {len(image_paths)}.")


    # ============================================================
    # PHASE 3: VOICEOVER (TTS)
    # ============================================================
    print("\n--- [Phase 3] Generating Voiceovers ---")
    
    scripts = lecture1.get_scripts(slides_content)
    
    audio_paths = voice.generate_audio_from_scripts(
        scripts=scripts,
        output_dir="output_audio"
    )

    # ============================================================
    # PHASE 4: VIDEO ASSEMBLY (MOVIEPY 2.2.1)
    # ============================================================
    print("\n--- [Phase 4] Assembling Video ---")

    if not MOVIEPY_AVAILABLE:
        print("❌ MoviePy not installed or import failed. Skipping video assembly.")
        return

    # Ensure we match images to audio
    num_slides = min(len(image_paths), len(audio_paths))
    
    if num_slides == 0:
        print("❌ Error: Missing images or audio. Cannot create video.")
        return

    clips = []
    
    print(f"Processing {num_slides} clips...")
    
    for i in range(num_slides):
        img_path = image_paths[i]
        audio_path = audio_paths[i]
        
        # Verify files exist
        if not os.path.exists(img_path) or not os.path.exists(audio_path):
            print(f"   Skipping Slide {i+1}: File missing.")
            continue
            
        try:
            # 1. Create Audio Clip
            audio_clip = AudioFileClip(audio_path)
            
            # 2. Create Image Clip (MoviePy 2.2.1 Syntax)
            # Use .with_duration() instead of .set_duration()
            # Use .with_audio() instead of .set_audio()
            
            slide_duration = audio_clip.duration + 0.25 # Add small pause
            
            image_clip = (
                ImageClip(img_path)
                .with_duration(slide_duration)
                .with_audio(audio_clip)
            )
            
            clips.append(image_clip)
            print(f"   + Added Slide {i+1} (Duration: {slide_duration:.2f}s)")
            
        except Exception as e:
            print(f"   ❌ Error assembling Slide {i+1}: {e}")

    if clips:
        print(f"\nRendering final video: {output_filename}...")
        
        try:
            # Concatenate
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Write File
            # Note: MoviePy 2.x still requires 'fps' for Image-based videos
            final_video.write_videofile(
                output_filename, 
                fps=24, 
                codec="libx264", 
                audio_codec="aac"
            )
            print(f"\n✅ DONE! Video saved to: {os.path.abspath(output_filename)}")
        except Exception as e:
            print(f"❌ Error during rendering: {e}")
            if "ffmpeg" in str(e).lower():
                print("   (This might be an FFMPEG path issue. Ensure FFMPEG is installed.)")
    else:
        print("❌ No valid clips created.")


if __name__ == "__main__":
    # Interactive Mode
    try:
        topic = "Bubble Sort Algorithm"
        print(f"--- Video Generator (MoviePy v2.2.1) ---")
        file = f"{topic.replace(' ', '_')}.mp4"
        generate_lecture_video(topic, file)
    except KeyboardInterrupt:
        print("\n\nUser aborted.")