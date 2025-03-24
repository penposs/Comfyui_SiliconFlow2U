# ComfyUI SiliconFlow2U 节点

这是一个用于 ComfyUI 的自定义节点，通过集成硅基流动 SiliconFlow API，让您能够在 ComfyUI 工作流中直接使用 DeepSeek 系列大语言模型和 通义万相Wan-AI \混元视频生成模型。
支持系统引导词设置人设，可以将 DeepSeek 赋予独特的角色特征，实现更个性化的文本生成。同时支持文本到视频和图像到视频的生成。



![节点界面预览](https://github.com/user-attachments/assets/6b5782d0-e17f-44bd-aaea-1932d50132aa)


## 🎯 主要特性

- 支持全系列 DeepSeek 模型
- 支持 Wan-AI 和腾讯混元视频生成模型
- 支持自定义模型人设（通过 System Prompt）
- 支持文本到视频和图像到视频的生成
- 一次配置 API Key，永久保存
- 简洁直观的操作界面

## 🔑 API Key 获取

您可以通过以下链接免费申请 SiliconFlow API Key：
[点击这里申请 API Key](https://cloud.siliconflow.cn/i/o9sYCl8W)

## 📦 安装方法

1. 克隆仓库到 ComfyUI 的 custom_nodes 目录：

bash
cd ComfyUI/custom_nodes
git clone https://github.com/penposs/Comfyui_SiliconFlow2U.git

2. 安装依赖：
bash
pip install -r requirements.txt

3. 重启 ComfyUI

## 🚀 使用方法

### 文本生成

1. 在节点浏览器中找到 "硅基流动2U"
2. 配置参数：
   - New API Key: 首次使用时输入 API Key（之后会自动保存）
   - Prompt: 输入提示词
   - Model: 选择模型
   - Max Tokens: 生成文本的最大长度
   - Temperature: 控制输出的随机性
   - System Prompt (可选): 设定模型人设

### 视频生成

1. 在节点浏览器中找到 "SiliconFlow Video"
2. 配置参数：
   - Prompt: 输入提示词，描述您想要生成的视频内容
   - Model: 选择视频生成模型
     - Wan-AI/Wan2.1-T2V-14B: 文本到视频模型
     - Wan-AI/Wan2.1-T2V-14B-Turbo: 快速版文本到视频模型
     - Wan-AI/Wan2.1-I2V-14B-720P: 图像到视频模型
     - Wan-AI/Wan2.1-I2V-14B-720P-Turbo: 快速版图像到视频模型
     - tencent/HunyuanVideo: 腾讯混元视频模型
   - Image Size: 选择输出视频分辨率（1280x720、720x1280 或 960x960）
   - Seed: 设置随机种子（0 表示随机）
   - Image (可选): 连接图像输入（仅 I2V 模型和混元视频模型需要）
   - Negative Prompt (可选): 设置负面提示词
   - New API Key (可选): 更新 API Key

注意事项：
- 对于图像到视频（I2V）模型，必须提供输入图像
- 图像会自动调整为所选的输出分辨率
- 视频生成可能需要一些时间，请耐心等待
- 生成完成后会返回视频的 URL 链接

## 📄 License

MIT License
