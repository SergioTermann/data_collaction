# PDF知识总结工具

这是一个使用智谱AI来读取PDF文件并总结其中主要知识点的工具。

## 功能特点

- 读取PDF文件内容
- 使用智谱AI的GLM-4.6模型总结文档内容
- 提取文档中的关键概念
- 支持命令行操作

## 安装

1. 克隆或下载本项目
2. 安装依赖包：

```bash
pip install -r requirements.txt
```

3. 复制`.env.example`文件为`.env`并填入您的智谱AI API密钥：

```bash
cp .env.example .env
```

然后编辑`.env`文件，设置您的API密钥：

```
ZHIPU_API_KEY=您的智谱AI_API密钥
```

## 使用方法

### 命令行使用

```bash
python main.py 您的PDF文件路径 [--api-key API密钥] [--output 输出文件路径]
```

参数说明：
- `pdf_path`：必需，PDF文件的路径
- `--api-key`, `-k`：可选，智谱AI的API密钥，如不提供则从环境变量获取
- `--output`, `-o`：可选，输出文件路径，如不提供则输出到控制台

### 示例

```bash
# 输出到控制台
python main.py document.pdf

# 指定API密钥并输出到文件
python main.py document.pdf --api-key YOUR_API_KEY --output summary.md
```

## 项目结构

- `main.py`：主程序入口
- `pdf_reader.py`：PDF文件读取模块
- `zhipu_ai.py`：智谱AI接口调用模块
- `pdf_summarizer.py`：PDF总结功能模块
- `requirements.txt`：项目依赖
- `.env.example`：环境变量示例文件

## 注意事项

- 智谱AI API有调用限制，请注意控制使用频率
- 对于大型PDF文件，程序会自动截取部分内容进行处理
- 处理结果的质量取决于PDF文本的提取质量和智谱AI模型的能力