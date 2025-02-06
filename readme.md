# ComfyUI SiliconFlow2U 节点

<<<<<<< HEAD
这是一个用于 ComfyUI 的自定义节点，通过集成 SiliconFlow API，让您能够在 ComfyUI 工作流中直接使用 DeepSeek 系列大语言模型。支持模型人设设定，可以将 DeepSeek 赋予独特的角色特征，实现更个性化的文本生成。
=======
这是一个用于 ComfyUI 的自定义节点，可以调用 SiliconFlow API 使用deepseek 魔法化提示词  支持给deepseek添加人设
![709dcaf05269fdbd44364c6a87ccf27](https://github.com/user-attachments/assets/6b5782d0-e17f-44bd-aaea-1932d50132aa)

硅基流动免费api_key申请链接
https://cloud.siliconflow.cn/i/o9sYCl8W

>>>>>>> 3c3e23cab45cc20ee804ca3ae791c4298818ca34

![节点界面预览](https://github.com/user-attachments/assets/6b5782d0-e17f-44bd-aaea-1932d50132aa)

## 🎯 主要特性

- 支持全系列 DeepSeek 模型
- 支持自定义模型人设（通过 System Prompt）
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

1. 在节点浏览器中找到 "硅基流动2U"
2. 配置参数：
   - New API Key: 首次使用时输入 API Key（之后会自动保存）
   - Prompt: 输入提示词
   - Model: 选择模型
   - Max Tokens: 生成文本的最大长度
   - Temperature: 控制输出的随机性
   - System Prompt (可选): 设定模型人设

## 📄 License

MIT License

<<<<<<< HEAD
=======
Copyright (c) 2024 penpos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
>>>>>>> 3c3e23cab45cc20ee804ca3ae791c4298818ca34
