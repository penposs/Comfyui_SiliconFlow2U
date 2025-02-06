import requests
import json
from .config import Config

class SiliconFlowNode:
    def __init__(self):
        self.config = Config()
        
    @classmethod
    def INPUT_TYPES(cls):
        config = Config()
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "model": (config.get_models(),),
                "max_tokens": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0}),
            },
            "optional": {
                "system_prompt": ("STRING", {"default": "", "multiline": True}),
                "new_api_key": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "SiliconFlow"

    def generate(self, prompt, model, max_tokens=512, temperature=0.7, system_prompt="", new_api_key=""):
        if new_api_key.strip():
            self.config.set_api_key(new_api_key.strip())
        
        api_key = self.config.get_api_key()
        if not api_key:
            return ("错误: 请先设置 API Key",)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        try:
            response = requests.post(
                self.config.get_api_base(),
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            return (result["choices"][0]["message"]["content"],)
        except Exception as e:
            print(f"Error calling SiliconFlow API: {str(e)}")
            return ("Error: " + str(e),) 