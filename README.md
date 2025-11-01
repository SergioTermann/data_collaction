# PDF Knowledge Summarizer

PDF Knowledge Summarizer是一个强大的PDF文档处理工具，利用智谱AI大模型自动提取和总结PDF文档中的关键信息，生成结构化的知识摘要。

## 主要功能

- **PDF文档总结**：自动分析PDF文档内容，生成结构化摘要
- **关键概念提取**：识别并解释文档中的重要概念和术语
- **问答式格式化**：将内容以问题形式呈现，便于理解和记忆
- **批量处理**：支持处理单个PDF文件或整个文件夹
- **进度显示**：实时显示文件处理进度
- **自定义处理说明**：允许用户添加个性化处理要求，指导AI生成更符合需求的内容

## 安装与配置

1. 克隆或下载本项目到本地
2. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```
3. 配置智谱AI API密钥：
   - 复制`.env.example`文件并重命名为`.env`
   - 在`.env`文件中填入您的智谱AI API密钥：
     ```
     ZHIPUAI_API_KEY=您的API密钥
     ```

## 使用方法

### 图形界面

1. 运行主程序：
   ```
   python main.py
   ```
2. 在打开的图形界面中：
   - 点击"选择PDF文件"处理单个PDF文件
   - 点击"选择文件夹"批量处理多个PDF文件
   - 在"自定义处理说明"框中输入特定要求（可选）
   - 处理完成后，结果将保存为Markdown文件在原PDF所在目录

### 命令行

也可以通过命令行使用：

```
python main.py --file path/to/your/file.pdf
python main.py --folder path/to/your/folder
```

## 输出格式

处理后的输出为Markdown格式，包含：
- 文档基本信息（文件名、页数）
- 内容摘要（结构化的文档总结）
- 关键概念（文档中的重要术语及解释）

## 技术栈

- Python 3.9+
- tkinter (GUI界面)
- PyPDF2 (PDF解析)
- 智谱AI GLM-4.6 大模型 (内容分析与生成)

## 注意事项

- 处理大型PDF文件可能需要较长时间
- API调用受智谱AI服务限制，请注意使用频率
- 对于非文本PDF（如扫描件）可能无法正确提取内容

A tool that uses ZhipuAI to read PDF files and summarize their key knowledge points.

## Features

- Read PDF file content
- Summarize document content using ZhipuAI's GLM-4.6 model
- Extract key concepts from documents
- Support for command line operation
- Modern graphical user interface

## Installation

1. Clone or download this project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the `.env.example` file to `.env` and add your ZhipuAI API key:

```bash
cp .env.example .env
```

Then edit the `.env` file and set your API key:

```
ZHIPU_API_KEY=your_zhipu_ai_api_key
```

## Usage

### Command Line Usage

```bash
python main.py your_pdf_file_path [--api-key API_KEY] [--output output_file_path]
```

Parameters:
- `pdf_path`: Required, path to the PDF file
- `--api-key`, `-k`: Optional, ZhipuAI API key, if not provided it will be retrieved from environment variables
- `--output`, `-o`: Optional, output file path, if not provided output will be sent to console

### Examples

```bash
# Output to console
python main.py document.pdf

# Specify API key and output to file
python main.py document.pdf --api-key YOUR_API_KEY --output summary.md
```

### Graphical Interface

You can also run the application with a graphical interface by simply running:

```bash
python main.py
```

or

```bash
python main.py --gui
```

## Project Structure

- `main.py`: Main program entry
- `pdf_reader.py`: PDF file reading module
- `zhipu_ai.py`: ZhipuAI API interface module
- `pdf_summarizer.py`: PDF summarization functionality module
- `requirements.txt`: Project dependencies
- `.env.example`: Example environment variable file

## Notes

- ZhipuAI API has usage limits, please be mindful of usage frequency
- For large PDF files, the program will automatically truncate content for processing
- The quality of results depends on the quality of PDF text extraction and the capabilities of the ZhipuAI model