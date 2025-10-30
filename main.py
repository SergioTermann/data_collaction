import argparse
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_summarizer import PDFSummarizer
from dotenv import load_dotenv
import time
import datetime

def process_pdf(pdf_path, api_key=None):
    """
    处理PDF文件并返回结果
    """
    try:
        # 初始化PDF总结器
        summarizer = PDFSummarizer(api_key=api_key)
        
        # 总结PDF内容
        print(f"正在处理PDF文件: {pdf_path}")
        result = summarizer.summarize_pdf(pdf_path)
        
        # 格式化输出内容
        output_content = f"""
# PDF文档总结

## 文件信息
- 文件: {os.path.basename(pdf_path)}
- 页数: {result['page_count']}
- 分析时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 内容总结
{result['summary']}

## 关键概念
{result['key_concepts']}
"""
        return output_content
    except Exception as e:
        raise Exception(f"处理PDF时出错: {str(e)}")

def save_to_markdown(content, pdf_path):
    """
    将内容保存为Markdown文件
    """
    # 生成默认的输出文件名（基于原PDF文件名）
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    default_output = f"{base_name}_summary.md"
    
    # 打开保存文件对话框
    output_path = filedialog.asksaveasfilename(
        defaultextension=".md",
        filetypes=[("Markdown文件", "*.md")],
        initialfile=default_output,
        title="保存分析结果"
    )
    
    # 如果用户取消了保存对话框，则返回None
    if not output_path:
        return None
    
    # 保存内容到文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path

def gui_mode():
    """
    图形界面模式
    """
    # 加载环境变量
    load_dotenv()
    
    # 创建主窗口
    root = tk.Tk()
    root.title("PDF知识总结工具")
    root.geometry("500x300")
    
    # 设置窗口样式
    root.configure(bg="#f0f0f0")
    
    # 创建标题标签
    title_label = tk.Label(
        root, 
        text="PDF知识总结工具", 
        font=("Arial", 18, "bold"),
        bg="#f0f0f0",
        pady=20
    )
    title_label.pack()
    
    # 创建说明标签
    info_label = tk.Label(
        root, 
        text="使用智谱AI分析PDF文档并提取主要知识点",
        bg="#f0f0f0",
        pady=10
    )
    info_label.pack()
    
    # 创建按钮框架
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=20)
    
    # 创建选择文件按钮
    def select_and_process_pdf():
        # 打开文件选择对话框
        pdf_path = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf")]
        )
        
        # 如果用户取消了文件选择，则返回
        if not pdf_path:
            return
        
        # 显示处理中的消息
        status_label.config(text="正在处理PDF文件，请稍候...")
        root.update()
        
        try:
            # 处理PDF文件
            api_key = os.getenv("ZHIPU_API_KEY")
            content = process_pdf(pdf_path, api_key)
            
            # 保存结果
            output_path = save_to_markdown(content, pdf_path)
            
            if output_path:
                status_label.config(text=f"分析完成！结果已保存到: {os.path.basename(output_path)}")
                messagebox.showinfo("处理完成", f"PDF分析结果已保存到:\n{output_path}")
            else:
                status_label.config(text="分析完成，但未保存结果")
        except Exception as e:
            status_label.config(text=f"错误: {str(e)}")
            messagebox.showerror("处理错误", str(e))
    
    select_button = tk.Button(
        button_frame,
        text="选择PDF文件",
        command=select_and_process_pdf,
        width=20,
        height=2,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold")
    )
    select_button.pack(side=tk.LEFT, padx=10)
    
    # 创建退出按钮
    exit_button = tk.Button(
        button_frame,
        text="退出",
        command=root.destroy,
        width=10,
        height=2,
        bg="#f44336",
        fg="white",
        font=("Arial", 10, "bold")
    )
    exit_button.pack(side=tk.LEFT, padx=10)
    
    # 创建状态标签
    status_label = tk.Label(
        root, 
        text="准备就绪，请选择PDF文件",
        bg="#f0f0f0",
        pady=10
    )
    status_label.pack()
    
    # 运行主循环
    root.mainloop()

def cli_mode():
    """
    命令行模式
    """
    # 加载环境变量
    load_dotenv()
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='使用智谱AI总结PDF文档内容')
    parser.add_argument('pdf_path', nargs='?', help='PDF文件路径')
    parser.add_argument('--api-key', '-k', help='智谱AI API密钥，如不提供则从环境变量ZHIPU_API_KEY获取')
    parser.add_argument('--output', '-o', help='输出文件路径，如不提供则输出到控制台')
    parser.add_argument('--gui', '-g', action='store_true', help='启用图形界面模式')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 如果指定了--gui参数或没有提供pdf_path，则启动图形界面模式
    if args.gui or not args.pdf_path:
        gui_mode()
        return
    
    # 检查PDF文件是否存在
    if not os.path.exists(args.pdf_path):
        print(f"错误: PDF文件不存在: {args.pdf_path}")
        sys.exit(1)
    
    try:
        # 处理PDF文件
        output_content = process_pdf(args.pdf_path, args.api_key)
        
        # 输出结果
        if args.output:
            # 输出到文件
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_content)
            print(f"总结已保存到: {args.output}")
        else:
            # 输出到控制台
            print("\n" + "="*50)
            print(output_content)
            print("="*50)
        
        print("处理完成!")
        
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)

def main():
    """
    主函数，根据参数决定使用命令行模式还是图形界面模式
    """
    # 如果没有命令行参数，则启动图形界面模式
    if len(sys.argv) == 1:
        gui_mode()
    else:
        cli_mode()

if __name__ == "__main__":
    main()