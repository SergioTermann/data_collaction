# PDF Knowledge Summarizer

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