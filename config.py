import os
import json

class Config:
    API_BASE = "https://api.siliconflow.cn/v1/chat/completions"  # 只在这里定义一次
    _instance = None

    MODELS = [
        "deepseek-ai/DeepSeek-R1",
        "Pro/deepseek-ai/DeepSeek-R1",
        "deepseek-ai/DeepSeek-V3",
        "Pro/deepseek-ai/DeepSeek-V3",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
        "Pro/deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        "Pro/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "Pro/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
        "meta-llama/Llama-3.3-70B-Instruct",
        "AIDC-AI/Marco-o1",
        "deepseek-ai/DeepSeek-V2.5",
        "Qwen/Qwen2.5-72B-Instruct-128K",
        "Qwen/Qwen2.5-72B-Instruct",
        "Qwen/Qwen2.5-32B-Instruct",
        "Qwen/Qwen2.5-14B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
        "Qwen/Qwen2.5-Coder-32B-Instruct",
        "Qwen/Qwen2.5-Coder-7B-Instruct",
        "Qwen/Qwen2-7B-Instruct",
        "Qwen/Qwen2-1.5B-Instruct",
        "Qwen/QwQ-32B-Preview",
        "TeleAI/TeleChat2",
        "01-ai/Yi-1.5-34B-Chat-16K",
        "01-ai/Yi-1.5-9B-Chat-16K",
        "01-ai/Yi-1.5-6B-Chat",
        "THUDM/glm-4-9b-chat",
        "Vendor-A/Qwen/Qwen2.5-72B-Instruct",
        "internlm/internlm2_5-7b-chat",
        "internlm/internlm2_5-20b-chat",
        "nvidia/Llama-3.1-Nemotron-70B-Instruct",
        "meta-llama/Meta-Llama-3.1-405B-Instruct",
        "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "google/gemma-2-27b-it",
        "google/gemma-2-9b-it",
        "Pro/Qwen/Qwen2.5-7B-Instruct",
        "Pro/Qwen/Qwen2-7B-Instruct",
        "Pro/Qwen/Qwen2-1.5B-Instruct",
        "Pro/THUDM/chatglm3-6b",
        "Pro/THUDM/glm-4-9b-chat",
        "Pro/meta-llama/Meta-Llama-3.1-8B-Instruct",
        "Pro/google/gemma-2-9b-it"
    ]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.config_path = os.path.join(os.path.dirname(__file__), "config.json")
            cls._instance.config = cls._instance.load_config()
        return cls._instance

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_config()
        else:
            # 如果配置文件不存在，创建默认配置
            default_config = self.get_default_config()
            self.save_config(default_config)
            return default_config

    def get_default_config(self):
        return {
            "api_key": "",
        }

    def save_config(self, config=None):
        if config is None:
            config = self.config
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def get_api_key(self):
        return self.config.get("api_key", "")

    def get_api_base(self):
        return self.API_BASE

    def get_models(self):
        return self.MODELS

    def set_api_key(self, api_key):
        if api_key and api_key != self.config.get("api_key", ""):
            self.config["api_key"] = api_key
            self.save_config() 