# ComfyUI SiliconFlow Node

这是一个用于 ComfyUI 的自定义节点，可以调用 SiliconFlow API 使用deepseek 魔法化提示词  支持给deepseek添加人设
![709dcaf05269fdbd44364c6a87ccf27](https://github.com/user-attachments/assets/6b5782d0-e17f-44bd-aaea-1932d50132aa)

硅基流动免费api_key申请链接
https://cloud.siliconflow.cn/i/o9sYCl8W


## 功能特点

- 支持所有 SiliconFlow 模型
- 可配置的生成参数（max_tokens, temperature）
- 支持系统提示词
- 简单易用的界面

## 安装

1. 将此仓库克隆到 ComfyUI 的 `custom_nodes` 目录：

bash
git clone https://github.com/yourusername/ComfyUI-SiliconFlow.git


启 ComfyUI

## 使用方法

1. 在节点浏览器中找到 "SiliconFlow Text Generation"
2. 配置以下参数：
   - API Key: 你的 SiliconFlow API 密钥
   - Prompt: 输入提示词
   - Model: 选择要使用的模型
   - Max Tokens: 生成文本的最大长度
   - Temperature: 控制输出的随机性
   - System Prompt (可选): 系统提示词

## License
MIT License

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
