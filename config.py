import os
import json

class Config:
    _instance = None

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
            "api_base": "https://api.siliconflow.cn/chat/completions",
            "models": [
                "deepseek-ai/DeepSeek-R1",
                "deepseek-ai/DeepSeek-V3",
                "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
                "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
                "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
                "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
                "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
                "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
                "meta-llama/Llama-3.3-70B-Instruct",
                "AIDC-AI/Marco-o1",
                "Qwen/Qwen2.5-72B-Instruct",
                "Qwen/Qwen2.5-32B-Instruct",
                "Qwen/Qwen2.5-14B-Instruct",
                "Qwen/Qwen2.5-7B-Instruct"
            ]
        }

    def save_config(self, config=None):
        if config is None:
            config = self.config
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def get_api_key(self):
        return self.config.get("api_key", "")

    def get_api_base(self):
        return self.config.get("api_base", "https://api.siliconflow.cn/chat/completions")

    def get_models(self):
        return self.config.get("models", [])

    def set_api_key(self, api_key):
        if api_key and api_key != self.config.get("api_key", ""):
            self.config["api_key"] = api_key
            self.save_config() 