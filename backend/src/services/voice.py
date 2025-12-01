import os
import time
from typing import List, Tuple, Optional

# Try imports for TTS engines
try:
    from openai import OpenAI
    from src.config import OPENAI_API_KEY
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OPENAI_API_KEY = None

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class VoiceGenerator:
    """
    Generate voiceover audio from text scripts.
    """

    def __init__(self, use_openai: bool = True):
        """
        Initialize voice generator.
        
        Args:
            use_openai: If True, use OpenAI TTS API; otherwise use local TTS
        """
        # Logic to determine which engine to use
        if use_openai and OPENAI_AVAILABLE and OPENAI_API_KEY:
            self.use_openai = True
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.voice = "alloy"  # Options: alloy, echo, fable, onyx, nova, shimmer
            self.model = "tts-1"  # Use "tts-1-hd" for higher quality if needed
            print("[VoiceGenerator] Initialized with OpenAI TTS.")
        elif PYTTSX3_AVAILABLE:
            self.use_openai = False
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
            print("[VoiceGenerator] Initialized with Local pyttsx3.")
        else:
            raise RuntimeError("No TTS engine available. Please install 'openai' or 'pyttsx3'.")

    def generate_audio_openai(self, text: str, output_path: str) -> None:
        """Generate audio using OpenAI TTS API."""
        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )
            response.stream_to_file(output_path)
        except Exception as e:
            raise RuntimeError(f"OpenAI TTS failed: {e}")

    def generate_audio_local(self, text: str, output_path: str) -> None:
        """Generate audio using local pyttsx3."""
        try:
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
        except Exception as e:
            raise RuntimeError(f"Local TTS failed: {e}")

    def generate_single_slide_audio(self, script: str, slide_index: int, output_dir: str) -> str:
        """
        Generate audio for a single slide script.
        Returns the path to the generated file.
        """
        if not script or not script.strip():
            print(f"   ⚠️ Slide {slide_index}: Script is empty, skipping audio.")
            return ""

        # Ensure filename matches slide index (e.g., slide_01.mp3)
        ext = "mp3" if self.use_openai else "wav"
        filename = f"slide_{slide_index:02d}.{ext}"
        output_path = os.path.join(output_dir, filename)

        # Generate
        if self.use_openai:
            self.generate_audio_openai(script, output_path)
        else:
            self.generate_audio_local(script, output_path)

        return output_path

# -----------------------------------------------------------
# MAIN FUNCTION TO PROCESS LIST OF SCRIPTS
# -----------------------------------------------------------

def generate_audio_from_scripts(
    scripts: List[str], 
    output_dir: str = "generated_audio"
) -> List[str]:
    """
    Takes the output of get_scripts(slides) and generates audio files one by one.
    
    Args:
        scripts: List[str] where index 0 is Slide 1, index 1 is Slide 2, etc.
        output_dir: Folder to save audio files.
        
    Returns:
        List[str]: List of paths to the generated audio files.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize generator (defaults to OpenAI if available)
    generator = VoiceGenerator(use_openai=True)
    
    generated_files = []

    print(f"\n🎙️  Starting Voiceover Generation for {len(scripts)} slides...")

    for i, script in enumerate(scripts, start=1):
        print(f"   Processing Slide {i}...", end="", flush=True)
        
        try:
            start_time = time.time()
            
            # Generate the file
            path = generator.generate_single_slide_audio(
                script=script, 
                slide_index=i, 
                output_dir=output_dir
            )
            
            if path:
                duration = time.time() - start_time
                generated_files.append(path)
                print(f" Done ({duration:.2f}s) -> {os.path.basename(path)}")
            else:
                print(" Skipped (Empty).")
                
        except Exception as e:
            print(f" Error: {e}")

    print(f"✅ Audio generation complete. Saved to: {output_dir}\n")
    return generated_files


# -----------------------------------------------------------
# DEMO / TEST
# -----------------------------------------------------------

if __name__ == "__main__":
    # Simulate the output from lecture1.py -> get_scripts(slides)
    # In a real scenario, you would import generate_audio_from_scripts into your main pipeline
    
    mock_scripts_from_lecture1 = [
        "Welcome to the lecture on Bubble Sort. This is a simple comparison-based algorithm.",
        "Here we see the first pass. We compare the first two elements, 5 and 3.",
        "Since 5 is greater than 3, we swap them. Now 3 is in the first position.",
        "We continue this process until the largest element bubbles to the end."
    ]

    print("--- Testing Voice Generation with Mock Scripts ---")
    paths = generate_audio_from_scripts(
        scripts=mock_scripts_from_lecture1,
        output_dir="test_audio_output"
    )
    
    print("Generated Files:", paths)