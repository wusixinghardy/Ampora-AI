import os
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, GEMINI_MODEL_NAME

class GeminiClient:
    """
    Wrapper for Google Gemini API requests.
    Designed to be a drop-in replacement for the ChatGPTClient.
    """

    def __init__(self, model: str | None = None):
        self.api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        # Default to a text model, but can be overridden for image gen
        self.model = model or "gemini-3-pro-image-preview" 

        if not self.api_key:
            raise RuntimeError("Missing GEMINI_API_KEY — please set it in .env")

        self.client = genai.Client(api_key=self.api_key)
        print(f"[DEBUG] Using Gemini model={self.model}")

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        """
        Send a prompt to the model and return text output.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[{
                    "role": "user",
                    "parts": [{"text": user_prompt}]
                }],
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.7,
                )
            )

            # Prefer the SDK's helper
            if response.text:
                return response.text.strip()

            # Fallback extraction
            if response.candidates:
                parts = response.candidates[0].content.parts
                for p in parts:
                    if hasattr(p, "text"):
                        return p.text.strip()

            return ""

        except Exception as e:
            raise RuntimeError(f"Gemini API error: {e}")

    def generate_image(self, prompt: str) -> bytes:
        """
        Generate an image using the Google Gen AI SDK.
        Supports both 'Imagen' models (via generate_images) and 'Gemini' image models (via generate_content).
        """
        print(f"[DEBUG] Generating image with model: {self.model}...")

        try:
            # -------------------------------------------------------
            # CASE 1: IMAGEN MODELS (e.g., 'imagen-3.0-generate-001')
            # -------------------------------------------------------
            if "imagen" in self.model.lower():
                response = self.client.models.generate_images(
                    model=self.model,
                    prompt=prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        aspect_ratio="16:9",  # Best for slides
                        include_rai_reasoning=True
                    )
                )
                if response.generated_images:
                    return response.generated_images[0].image.image_bytes
                else:
                    raise RuntimeError("Imagen returned no images.")

            # -------------------------------------------------------
            # CASE 2: GEMINI MODELS (e.g., 'gemini-3-pro-image-preview')
            # -------------------------------------------------------
            else:
                # Gemini models generate images via generate_content with specific prompting
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                
                # Extract inline image data from the response parts
                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if part.inline_data:
                            return part.inline_data.data  # This is the raw bytes
                
                raise RuntimeError("Gemini response contained no inline image data.")

        except Exception as e:
            raise RuntimeError(f"Gemini Image Generation failed: {e}")


if __name__ == "__main__":
    try:
        client = GeminiClient()
        print("Sending chat message...")
        reply = client.chat(
            system_prompt="You are a helpful coding assistant.",
            user_prompt="Hello! Write a one-line Python list comprehension."
        )
        print("Response:", reply)
    except Exception as err:
        print("Error:", err)