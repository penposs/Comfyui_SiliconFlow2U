import os
import json
# 可选依赖：requests 不存在时回退到 urllib
try:
    import requests  # type: ignore
except Exception:  # noqa: F401
    requests = None  # type: ignore
import urllib.request
import urllib.error

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
    # 视频模型的回退列表（当在线拉取失败时使用）
    VIDEO_MODELS = [
        "Wan-AI/Wan2.1-T2V-14B",
        "Wan-AI/Wan2.1-T2V-14B-Turbo",
        "Wan-AI/Wan2.1-I2V-14B-720P",
        "Wan-AI/Wan2.1-I2V-14B-720P-Turbo",
        "tencent/HunyuanVideo"
    ]

    # 新增：视觉多模态模型的静态回退列表（当在线拉取失败时使用）
    VISION_MODELS = [
        "THUDM/glm-4v-9b",
        "zai-org/GLM-4.5V",
        "Qwen/Qwen2-VL-7B-Instruct",
        "Qwen/Qwen2.5-VL-7B-Instruct",
        "Qwen/Qwen2.5-VL-32B-Instruct",
        "Qwen/Qwen2.5-VL-72B-Instruct",
        "deepseek-ai/DeepSeek-VL2",
        "deepseek-ai/DeepSeek-VL2-Turbo",
    ]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.config_path = os.path.join(os.path.dirname(__file__), "config.json")
            cls._instance.config = cls._instance.load_config()
            # 启动时尝试从官方接口刷新模型列表（失败则静默回退到静态列表）
            try:
                print("[硅基流动2U] 正在尝试刷新文本/多模态模型列表...")
                ok = cls._instance.refresh_models_from_api()
                if not ok:
                    print("[硅基流动2U] 刷新文本/多模态模型列表失败，已使用内置静态列表")
            except Exception as e:
                print(f"[硅基流动2U] 刷新文本/多模态模型时异常: {str(e)}，已使用内置静态列表")
            # 同步刷新视频模型列表
            try:
                print("[硅基流动2U] 正在尝试刷新视频模型列表...")
                okv = cls._instance.refresh_video_models_from_api()
                if not okv:
                    print("[硅基流动2U] 刷新视频模型列表失败，已使用内置静态列表")
            except Exception as e:
                print(f"[硅基流动2U] 刷新视频模型时异常: {str(e)}，已使用内置静态列表")
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

    def refresh_models_from_api(self):
        """从官方接口拉取模型列表并更新到 MODELS。失败则保持原配置。"""
        url = "https://api.siliconflow.cn/v1/models"
        headers = {}
        api_key = self.get_api_key()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        try:
            data = None
            # 优先使用 requests
            if requests is not None:
                try:
                    resp = requests.get(url, headers=headers, timeout=15)
                    if resp.status_code == 200:
                        data = resp.json()
                except Exception:
                    data = None
            # 回退到 urllib
            if data is None:
                req = urllib.request.Request(url, headers=headers, method="GET")
                with urllib.request.urlopen(req, timeout=15) as r:
                    raw = r.read().decode("utf-8", errors="ignore")
                    data = json.loads(raw)
            model_ids = []
            # 兼容常见返回结构：{"data":[{"id":"model"}, ...]}
            if isinstance(data, dict):
                items = data.get("data") or data.get("models")
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            mid = item.get("id") or item.get("name")
                            if isinstance(mid, str):
                                model_ids.append(mid)
                        elif isinstance(item, str):
                            model_ids.append(item)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        mid = item.get("id") or item.get("name")
                        if isinstance(mid, str):
                            model_ids.append(mid)
                    elif isinstance(item, str):
                        model_ids.append(item)
            # 去重并更新
            if model_ids:
                seen = set()
                cleaned = []
                for m in model_ids:
                    if m not in seen:
                        seen.add(m)
                        cleaned.append(m)
                type(self).MODELS = cleaned
                print(f"[硅基流动2U] 已从官方接口刷新模型列表，共 {len(cleaned)} 个")
                return True
        except Exception as e:
            print(f"[硅基流动2U] 刷新文本/多模态模型失败: {str(e)}")
            return False
        return False

    def get_models(self):
        return self.MODELS

    # 新增：拉取视频模型列表
    def refresh_video_models_from_api(self):
        """仅拉取视频类模型（type=video），成功时更新到 VIDEO_MODELS。"""
        url = "https://api.siliconflow.cn/v1/models?type=video"
        headers = {}
        api_key = self.get_api_key()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        try:
            data = None
            if requests is not None:
                try:
                    resp = requests.get(url, headers=headers, timeout=15)
                    if resp.status_code == 200:
                        data = resp.json()
                except Exception:
                    data = None
            if data is None:
                req = urllib.request.Request(url, headers=headers, method="GET")
                with urllib.request.urlopen(req, timeout=15) as r:
                    raw = r.read().decode("utf-8", errors="ignore")
                    data = json.loads(raw)
            model_ids = []
            if isinstance(data, dict):
                items = data.get("data") or data.get("models")
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            mid = item.get("id") or item.get("name")
                            if isinstance(mid, str):
                                model_ids.append(mid)
                        elif isinstance(item, str):
                            model_ids.append(item)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        mid = item.get("id") or item.get("name")
                        if isinstance(mid, str):
                            model_ids.append(mid)
                    elif isinstance(item, str):
                        model_ids.append(item)
            if model_ids:
                seen = set()
                cleaned = []
                for m in model_ids:
                    if m not in seen:
                        seen.add(m)
                        cleaned.append(m)
                type(self).VIDEO_MODELS = cleaned
                print(f"[硅基流动2U] 已从官方接口刷新视频模型列表，共 {len(cleaned)} 个")
                return True
        except Exception as e:
            print(f"[硅基流动2U] 刷新视频模型失败: {str(e)}")
            return False
        return False

    def get_models(self):
        return self.MODELS

    # 新增：获取视频模型列表
    def get_video_models(self):
        return self.VIDEO_MODELS

    # 新增：获取视觉多模态模型列表
    def get_vision_models(self):
        return self.VISION_MODELS

    # 新增：获取全部模型（文本 + 视觉），去重并保持顺序
    def get_all_models(self):
        return list(dict.fromkeys(list(self.MODELS) + list(self.VISION_MODELS)))

    def set_api_key(self, api_key):
        if api_key and api_key != self.config.get("api_key", ""):
            self.config["api_key"] = api_key
            self.save_config()