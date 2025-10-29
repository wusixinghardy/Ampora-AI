import os
import requests
from src.config import OPENAI_API_KEY, OPENAI_API_BASE, MODEL_NAME


class ChatGPTClient:
    """
    Wrapper for OpenAI-style Chat API requests.
    """

    def __init__(self, model: str | None = None):
        self.api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        self.api_base = OPENAI_API_BASE or "https://api.openai.com/v1"
        self.model = model or MODEL_NAME or "gpt-5"

        if not self.api_key:
            raise RuntimeError("Missing OPENAI_API_KEY — please set it in .env")
        
        print(f"[DEBUG] Using model={self.model} | base={self.api_base}")

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        """
        Send a prompt to the model and return text output.
        """
        url = f"{self.api_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        response = requests.post(url, headers=headers, json=payload, timeout=(20, 300))

        if response.status_code != 200:
            raise RuntimeError(
                f"OpenAI API error {response.status_code}: {response.text}"
            )

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise RuntimeError(f"Unexpected API response: {data}") from e