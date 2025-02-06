import requests
import json
from .config import Config
import time

class SiliconFlowNode:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        
    @classmethod
    def INPUT_TYPES(cls):
        config = Config()
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "model": (config.get_models(),),
                "max_tokens": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0}),
                "top_p": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0}),
                "top_k": ("INT", {"default": 50, "min": 1, "max": 100}),
                "frequency_penalty": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 2.0}),
            },
            "optional": {
                "system_prompt": ("STRING", {"default": "", "multiline": True}),
                "new_api_key": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "SiliconFlow"

    def generate(self, prompt, model, max_tokens=512, temperature=0.7, top_p=0.7, 
                top_k=50, frequency_penalty=0.5, system_prompt="", new_api_key=""):
        try:
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
                "stream": False,
                "max_tokens": max_tokens,
                "stop": ["null"],
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "frequency_penalty": frequency_penalty,
                "n": 1,
                "response_format": {
                    "type": "text"
                }
            }

            print(f"\n[硅基流动2U] 正在调用 API...")
            print(f"[硅基流动2U] 模型: {model}")
            print(f"[硅基流动2U] 提示词: {prompt}")
            if system_prompt:
                print(f"[硅基流动2U] 系统提示词: {system_prompt}")

            start_time = time.time()
            response = self.session.post(
                self.config.get_api_base(),
                headers=headers,
                json=payload,
                timeout=300
            )
            end_time = time.time()
            
            print(f"[硅基流动2U] API 调用耗时: {end_time - start_time:.2f} 秒")

            if response.status_code != 200:
                error_msg = f"API 请求失败 (状态码: {response.status_code})"
                if response.status_code == 401:
                    error_msg = "API Key 无效或已过期"
                elif response.status_code == 429:
                    error_msg = "请求太频繁，请稍后再试"
                elif response.status_code >= 500:
                    error_msg = "服务器错误，请稍后重试"
                print(f"[硅基流动2U] 错误: {error_msg}")
                return (f"错误: {error_msg}",)

            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0].get("message", {}).get("content", "")
                print(f"[硅基流动2U] 生成完成，长度: {len(content)} 字符")
                return (content,)
            else:
                print("[硅基流动2U] 错误: API 返回数据格式异常")
                return ("错误: API 返回数据格式异常",)

        except requests.exceptions.Timeout:
            print("[硅基流动2U] 错误: API 请求超时")
            return ("错误: API 请求超时，请稍后重试",)
        except requests.exceptions.ConnectionError:
            print("[硅基流动2U] 错误: 无法连接到服务器")
            return ("错误: 无法连接到服务器，请检查网络连接",)
        except Exception as e:
            print(f"[硅基流动2U] 错误: {str(e)}")
            return (f"错误: {str(e)}",) 