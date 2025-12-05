import os
import time
import concurrent.futures
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
        # Logic to determine which engine to use
        if use_openai and OPENAI_AVAILABLE and OPENAI_API_KEY:
            self.use_openai = True
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.voice = "alloy"  
            self.model = "tts-1" 
        elif PYTTSX3_AVAILABLE:
            self.use_openai = False
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
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
        # Note: Local TTS is NOT thread-safe usually, but OpenAI API is.
        try:
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
        except Exception as e:
            raise RuntimeError(f"Local TTS failed: {e}")

    def generate_single_slide_audio(self, script: str, slide_index: int, output_dir: str) -> str:
        if not script or not script.strip():
            return ""

        ext = "mp3" if self.use_openai else "wav"
        filename = f"slide_{slide_index:02d}.{ext}"
        output_path = os.path.join(output_dir, filename)

        if self.use_openai:
            self.generate_audio_openai(script, output_path)
        else:
            self.generate_audio_local(script, output_path)

        return output_path

# -----------------------------------------------------------
# HELPER FOR PARALLEL EXECUTION
# -----------------------------------------------------------

def _process_single_audio_task(generator, script, idx, output_dir):
    """Helper to run inside a thread."""
    try:
        path = generator.generate_single_slide_audio(script, idx, output_dir)
        if path:
            print(f"   [Done] Audio {idx} saved.")
        else:
            print(f"   [Skip] Audio {idx} empty.")
        return idx, path
    except Exception as e:
        print(f"   [ERROR] Audio {idx} failed: {e}")
        return idx, None

# -----------------------------------------------------------
# MAIN FUNCTION (PARALLELIZED)
# -----------------------------------------------------------

def generate_audio_from_scripts(
    scripts: List[str], 
    output_dir: str = "generated_audio",
    max_workers: int = 5
) -> List[str]:
    """
    Generates audio files in PARALLEL using ThreadPoolExecutor.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # We create ONE generator instance. 
    # OpenAI client is thread-safe. Local pyttsx3 is NOT thread-safe.
    # We assume you are using OpenAI here. If using local, set max_workers=1.
    generator = VoiceGenerator(use_openai=True)
    
    # If using local engine, force sequential because pyttsx3 loop will break in threads
    if not generator.use_openai:
        print("⚠️ Local TTS detected. Forcing sequential execution (not thread-safe).")
        max_workers = 1

    generated_files = [None] * len(scripts)
    print(f"\n🎙️  Starting PARALLEL Voiceover (Workers: {max_workers})...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(_process_single_audio_task, generator, script, i, output_dir): i
            for i, script in enumerate(scripts, start=1)
        }

        # Collect results as they finish
        for future in concurrent.futures.as_completed(futures):
            idx, path = future.result()
            if path:
                generated_files[idx-1] = path

    # Filter out failures
    valid_files = [f for f in generated_files if f is not None]
    
    print(f"✅ Audio generation complete. {len(valid_files)}/{len(scripts)} success.\n")
    return valid_files

if __name__ == "__main__":
    # Test script
    mock_scripts = ["Hello world"] * 5
    generate_audio_from_scripts(mock_scripts, "test_audio")