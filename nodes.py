import requests
import json
from .config import Config
import time
import base64
import os
import time
from io import BytesIO
from PIL import Image
import numpy as np
import torch

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
                "model": (config.get_all_models(),),
                "max_tokens": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0}),
                "top_p": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0}),
                "top_k": ("INT", {"default": 50, "min": 1, "max": 100}),
                "frequency_penalty": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 2.0}),
            },
            "optional": {
                "system_prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE", {}),
                "image_detail": (["auto", "high", "low"],),
                "new_api_key": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "SiliconFlow"

    def generate(self, prompt, model, max_tokens=512, temperature=0.7, top_p=0.7, 
                top_k=50, frequency_penalty=0.5, system_prompt="", image=None, image_detail="auto", new_api_key=""):
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

            # 预处理图像（若提供）并转为 data:image/png;base64
            image_data_url = None
            if image is not None:
                try:
                    img = None
                    if isinstance(image, torch.Tensor):
                        img = image.detach().cpu().numpy()
                        if len(img.shape) == 4:
                            img = img.squeeze(0)
                        # 如果是 CHW，则转为 HWC
                        if img.shape[0] in (1, 3, 4):
                            if img.shape[0] == 1:
                                img = np.repeat(img, 3, axis=0)
                            elif img.shape[0] == 4:
                                img = img[:3]
                            img = img.transpose(1, 2, 0)
                        if img.max() <= 1.0:
                            img = (img * 255).astype('uint8')
                        else:
                            img = img.astype('uint8')
                    elif isinstance(image, np.ndarray):
                        img = image
                        if len(img.shape) == 2:
                            img = np.stack([img] * 3, axis=2)
                        elif len(img.shape) == 3:
                            if img.shape[2] == 1:
                                img = np.repeat(img, 3, axis=2)
                            elif img.shape[2] == 4:
                                img = img[..., :3]
                        if img.max() <= 1.0:
                            img = (img * 255).astype('uint8')
                        else:
                            img = img.astype('uint8')
                    elif isinstance(image, Image.Image):
                        img = np.array(image.convert("RGB"), dtype=np.uint8)
                    
                    if img is not None:
                        pil_img = Image.fromarray(img)
                        png_buffer = BytesIO()
                        pil_img.save(png_buffer, format="PNG")
                        png_bytes = png_buffer.getvalue()
                        base64_image = base64.b64encode(png_bytes).decode('utf-8')
                        image_data_url = f"data:image/png;base64,{base64_image}"
                        print("[硅基流动2U] 已附带图像输入（PNG Base64）")
                except Exception as e:
                    print(f"[硅基流动2U] 警告: 图像处理失败，将仅发送文本。原因: {str(e)}")
                    image_data_url = None

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            if image_data_url:
                content_parts = []
                if prompt:
                    content_parts.append({"type": "text", "text": prompt})
                content_parts.append({"type": "image_url", "image_url": {"url": image_data_url, "detail": image_detail}})
                messages.append({"role": "user", "content": content_parts})
            else:
                messages.append({"role": "user", "content": prompt})

            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p
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
                try:
                    err_body = response.text
                    if err_body:
                        print(f"[硅基流动2U] 服务端错误详情: {err_body}")
                        if len(err_body) < 2000:
                            return (f"错误: {error_msg} | 详情: {err_body}",)
                except Exception:
                    pass
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

class SiliconFlowVideoNode:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        
    @classmethod
    def INPUT_TYPES(cls):
        config = Config()
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "model": (config.get_video_models(),),
                "image_size": (["1280x720", "720x1280", "960x960"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2147483647}),
            },
            "optional": {
                "image": ("IMAGE", {}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True}),
                "new_api_key": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_video"
    CATEGORY = "SiliconFlow"

    def generate_video(self, prompt, model, image_size, seed=0, image=None, negative_prompt="", new_api_key=""):
        try:
            if new_api_key.strip():
                self.config.set_api_key(new_api_key.strip())
            
            api_key = self.config.get_api_key()
            if not api_key:
                print("[硅基流动2U] 错误: 请先设置 API Key")
                return ("",)
                
            # 检查是否需要图像输入
            needs_image = "I2V" in model or "Hunyuan" in model
            if needs_image and image is None:
                print(f"[硅基流动2U] 错误: 模型 {model} 需要图像输入")
                return ("",)

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": model,
                "prompt": prompt,
                "image_size": image_size,
                "seed": int(seed) if seed != 0 else int(time.time()) % 2147483647
            }
            
            if negative_prompt:
                payload["negative_prompt"] = negative_prompt
                
            # 处理图像输入
            if image is not None:
                try:
                    # 将图像转换为 PIL Image
                    if isinstance(image, torch.Tensor):
                        image = image.cpu().numpy()
                        if len(image.shape) == 4:
                            image = image.squeeze(0)  # 移除批次维度
                        if image.shape[0] == 3:  # CHW -> HWC
                            image = image.transpose(1, 2, 0)
                        elif image.shape[0] == 1:  # 单通道 -> RGB
                            image = np.repeat(image.transpose(1, 2, 0), 3, axis=2)
                        elif image.shape[0] == 4:  # RGBA -> RGB
                            image = image[:3].transpose(1, 2, 0)
                        
                        if image.max() <= 1.0:
                            image = (image * 255).astype('uint8')
                        else:
                            image = image.astype('uint8')
                    elif isinstance(image, np.ndarray):
                        if len(image.shape) == 2:  # 灰度图
                            image = np.stack([image] * 3, axis=2)
                        elif len(image.shape) == 3:
                            if image.shape[2] == 1:  # 单通道
                                image = np.repeat(image, 3, axis=2)
                            elif image.shape[2] == 4:  # RGBA
                                image = image[..., :3]
                        
                        if image.max() <= 1.0:
                            image = (image * 255).astype('uint8')
                        else:
                            image = image.astype('uint8')
                    
                    # 转换为 PIL Image
                    image = Image.fromarray(image)
                    
                    # 调整图像大小
                    target_width, target_height = map(int, image_size.split('x'))
                    if image.size != (target_width, target_height):
                        image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    
                    # 转换为 WebP 格式
                    webp_buffer = BytesIO()
                    image.save(webp_buffer, format="WEBP", quality=100)
                    webp_data = webp_buffer.getvalue()
                    
                    # 转换为 Base64
                    base64_image = base64.b64encode(webp_data).decode('utf-8')
                    payload["image"] = f"data:image/webp;base64,{base64_image}"
                    print(f"[硅基流动2U] 图像已处理并转换为 WebP Base64 格式")
                    
                except Exception as e:
                    print(f"[硅基流动2U] 错误: 图像处理失败: {str(e)}")
                    return ("",)
            elif needs_image:
                print(f"[硅基流动2U] 错误: 模型 {model} 需要图像输入")
                return ("",)

            print(f"\n[硅基流动2U] 正在提交视频生成请求...")
            print(f"[硅基流动2U] 模型: {model}")
            print(f"[硅基流动2U] 提示词: {prompt}")
            if negative_prompt:
                print(f"[硅基流动2U] 负面提示词: {negative_prompt}")

            # 步骤1：提交视频生成请求
            submit_url = "https://api.siliconflow.cn/v1/video/submit"
            try:
                submit_response = self.session.post(
                    submit_url,
                    headers=headers,
                    json=payload,
                    timeout=60
                )
            except requests.exceptions.RequestException as e:
                print(f"[硅基流动2U] 错误: 请求错误: {str(e)}")
                return ("",)
            
            if submit_response.status_code != 200:
                error_msg = f"视频生成请求失败 (状态码: {submit_response.status_code})"
                if submit_response.status_code == 401:
                    error_msg = "API Key 无效或已过期"
                elif submit_response.status_code == 429:
                    error_msg = "请求太频繁，请稍后再试"
                elif submit_response.status_code >= 500:
                    error_msg = "服务器错误，请稍后重试"
                print(f"[硅基流动2U] 错误: {error_msg}")
                return ("",)

            try:
                submit_result = submit_response.json()
                if "requestId" not in submit_result:
                    print("[硅基流动2U] 错误: 视频生成提交失败，未返回requestId")
                    print(f"[硅基流动2U] 响应内容: {json.dumps(submit_result, ensure_ascii=False)}")
                    return ("",)
            except json.JSONDecodeError:
                print("[硅基流动2U] 错误: 无法解析API响应")
                print(f"[硅基流动2U] 响应内容: {submit_response.text}")
                return ("",)
                
            request_id = submit_result["requestId"]
            print(f"[硅基流动2U] 视频生成请求已提交，requestId: {request_id}")
            
            # 步骤2：轮询视频生成状态
            status_url = "https://api.siliconflow.cn/v1/video/status"
            status_payload = {
                "requestId": request_id
            }
            
            max_retries = 30
            retry_count = 0
            wait_time = 5
            
            while retry_count < max_retries:
                print(f"[硅基流动2U] 正在检查视频生成状态 (第{retry_count+1}次)...")
                retry_count += 1
                
                try:
                    status_response = self.session.post(
                        status_url,
                        headers=headers,
                        json=status_payload,
                        timeout=60
                    )
                    
                    if status_response.status_code != 200:
                        print(f"[硅基流动2U] 错误: 获取视频状态失败 (状态码: {status_response.status_code})")
                        time.sleep(wait_time)
                        continue
                        
                    status_result = status_response.json()
                    if not isinstance(status_result, dict):
                        print("[硅基流动2U] 错误: 状态响应格式错误")
                        return ("",)
                        
                    current_status = status_result.get("status")
                    if not current_status:
                        print("[硅基流动2U] 错误: 响应中缺少状态信息")
                        return ("",)
                    
                    if current_status == "Succeed":
                        print("[硅基流动2U] 视频生成成功!")
                        videos = status_result.get("results", {}).get("videos", [])
                        if not videos:
                            print("[硅基流动2U] 错误: 未找到视频结果")
                            return ("",)
                            
                        video_url = videos[0].get("url")
                        if not video_url:
                            print("[硅基流动2U] 错误: 未找到视频链接")
                            return ("",)
                            
                        print(f"[硅基流动2U] 视频链接: {video_url}")
                        return (video_url,)
                        
                    elif current_status == "Failed":
                        reason = status_result.get("reason", "未知原因")
                        print(f"[硅基流动2U] 错误: 视频生成失败，原因: {reason}")
                        return ("",)
                        
                    elif current_status in ["InQueue", "InProgress"]:
                        status_text = "排队中" if current_status == "InQueue" else "生成中"
                        print(f"[硅基流动2U] 视频{status_text}，等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                        wait_time = min(wait_time * 1.5, 30)
                        continue
                        
                    else:
                        print(f"[硅基流动2U] 未知状态: {current_status}")
                        return ("",)
                        
                except requests.exceptions.RequestException as e:
                    print(f"[硅基流动2U] 检查状态时发生错误: {str(e)}")
                    time.sleep(wait_time)
                    continue
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    print(f"[硅基流动2U] 解析状态响应失败: {str(e)}")
                    return ("",)
            
            print("[硅基流动2U] 错误: 视频生成超时，请稍后检查结果")
            return ("",)
            
        except requests.exceptions.Timeout:
            print("[硅基流动2U] 错误: API 请求超时")
            return ("",)
        except requests.exceptions.ConnectionError:
            print("[硅基流动2U] 错误: 无法连接到服务器")
            return ("",)
        except Exception as e:
            print(f"[硅基流动2U] 错误: {str(e)}")
            return ("",)

class SiliconFlowUploadNode:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "", "multiline": False}),
                "purpose": (["batch"],),
            },
            "optional": {
                "new_api_key": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "upload_file"
    CATEGORY = "SiliconFlow"

    def upload_file(self, file_path, purpose="batch", new_api_key=""):
        try:
            if new_api_key.strip():
                self.config.set_api_key(new_api_key.strip())
            
            api_key = self.config.get_api_key()
            if not api_key:
                return ("错误: 请先设置 API Key",)
                
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return (f"错误: 文件不存在: {file_path}",)
                
            # 检查文件是否可读
            if not os.access(file_path, os.R_OK):
                return (f"错误: 无法读取文件: {file_path}",)

            headers = {
                "Authorization": f"Bearer {api_key}"
                # 注意：这里不设置 Content-Type，因为 requests 会自动设置为 multipart/form-data
            }

            # 准备文件数据
            files = {
                'file': (os.path.basename(file_path), open(file_path, 'rb')),
            }
            
            # 准备其他表单数据
            data = {
                'purpose': purpose
            }

            print(f"\n[硅基流动2U] 正在上传文件...")
            print(f"[硅基流动2U] 文件路径: {file_path}")
            print(f"[硅基流动2U] 文件名: {os.path.basename(file_path)}")
            print(f"[硅基流动2U] 用途: {purpose}")

            # 发送上传请求
            upload_url = "https://api.siliconflow.cn/v1/files"
            start_time = time.time()
            response = self.session.post(
                upload_url,
                headers=headers,
                files=files,
                data=data,
                timeout=300
            )
            end_time = time.time()
            
            print(f"[硅基流动2U] 文件上传耗时: {end_time - start_time:.2f} 秒")

            if response.status_code != 200:
                error_msg = f"文件上传失败 (状态码: {response.status_code})"
                if response.status_code == 401:
                    error_msg = "API Key 无效或已过期"
                elif response.status_code == 429:
                    error_msg = "请求太频繁，请稍后再试"
                elif response.status_code >= 500:
                    error_msg = "服务器错误，请稍后重试"
                print(f"[硅基流动2U] 错误: {error_msg}")
                return (f"错误: {error_msg}",)

            result = response.json()
            if result.get("status") == True and "data" in result:
                file_data = result["data"]
                file_id = file_data.get("id", "未知")
                file_size = file_data.get("bytes", 0)
                file_name = file_data.get("filename", "未知")
                created_at = file_data.get("createdAt", 0)
                
                # 格式化时间戳为可读时间
                if created_at:
                    created_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_at))
                else:
                    created_time = "未知"
                
                print(f"[硅基流动2U] 文件上传成功!")
                print(f"[硅基流动2U] 文件ID: {file_id}")
                print(f"[硅基流动2U] 文件名: {file_name}")
                print(f"[硅基流动2U] 文件大小: {file_size} 字节")
                print(f"[硅基流动2U] 创建时间: {created_time}")
                
                # 返回文件ID，便于直接连接到视频生成节点
                return (file_id,)
            else:
                print("[硅基流动2U] 错误: API 返回数据格式异常")
                print(f"[硅基流动2U] 响应内容: {json.dumps(result, ensure_ascii=False)}")
                return ("错误: API 返回数据格式异常",)
                
        except Exception as e:
            print(f"[硅基流动2U] 错误: {str(e)}")
            return (f"错误: {str(e)}",)