import argparse
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from pdf_summarizer import PDFSummarizer
from dotenv import load_dotenv
import time
import datetime


def process_pdf(pdf_path, api_key=None, as_questions=True):
    """
    Process PDF file and return results in knowledge base friendly markdown format
    
    Args:
        pdf_path: Path to PDF file
        api_key: API key for ZhipuAI
        as_questions: If True, format summary and concepts as questions when possible
    """
    try:
        # Initialize PDF summarizer
        summarizer = PDFSummarizer(api_key=api_key)
        
        # Summarize PDF content
        print(f"Processing PDF file: {pdf_path}")
        result = summarizer.summarize_pdf(pdf_path, as_questions=as_questions)
        
        # Get filename without extension for title
        filename = os.path.basename(pdf_path)
        title = os.path.splitext(filename)[0]
        title_slug = title.lower().replace(' ', '_')
        current_year = datetime.datetime.now().strftime('%Y')
        page_count = result['page_count']
        
        # Create citation template separately
        citation = f"@article{{{title_slug},\n  title={{{title}}},\n  author={{}},\n  pages={{{page_count}}},\n  year={{{current_year}}}\n}}"
        
        # Format output content in knowledge base friendly format
        output_content = f"""---
title: {title}
description: 自动生成的PDF文档摘要和关键概念
date: {datetime.datetime.now().strftime('%Y-%m-%d')}
tags:
  - 文档摘要
  - PDF
  - 知识库
---

# {title}

> [!info] 文件信息
> - **原始文件**: {filename}
> - **页数**: {result['page_count']}
> - **分析时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 内容摘要

{result['summary']}

## 关键概念

{result['key_concepts']}

## 引用方式

```
{citation}
```
"""
        return output_content
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")


def process_folder(folder_path, api_key=None, as_questions=True):
    """
    处理文件夹中的所有PDF文件，并在同一文件夹中生成同名的Markdown文件
    
    Args:
        folder_path: 文件夹路径
        api_key: ZhipuAI的API密钥
        as_questions: 如果为True，尽可能将摘要和概念格式化为问题
    """
    processed_files = []
    errors = []
    
    # 获取文件夹中的所有PDF文件
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        raise Exception(f"在文件夹 {folder_path} 中未找到PDF文件")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        try:
            # 处理PDF文件
            content = process_pdf(pdf_path, api_key, as_questions)
            
            # 生成输出文件名（与原PDF文件同名，但扩展名为.md）
            base_name = os.path.splitext(pdf_file)[0]
            output_path = os.path.join(folder_path, f"{base_name}.md")
            
            # 保存内容到文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            processed_files.append(output_path)
            
        except Exception as e:
            errors.append(f"{pdf_file}: {str(e)}")
    
    return {
        "processed_files": processed_files,
        "errors": errors,
        "total_processed": len(processed_files),
        "total_errors": len(errors)
    }
def save_to_markdown(content, pdf_path):
    """
    Save content to Markdown file optimized for knowledge base
    """
    # Generate default output filename (based on original PDF filename)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    default_output = f"{base_name}.md"
    
    # Open save file dialog
    output_path = filedialog.asksaveasfilename(
        defaultextension=".md",
        filetypes=[("Markdown Files", "*.md")],
        initialfile=default_output,
        title="保存知识库文档"
    )
    
    # If user cancels the save dialog, return None
    if not output_path:
        return None
    
    # Save content to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path


def gui_mode():
    """
    Graphical User Interface mode
    """
    # Load environment variables
    load_dotenv()
    
    # Create main window
    root = tk.Tk()
    root.title("PDF知识提取器 - 北京风起时域科技有限公司")
    root.geometry("800x650")
    root.minsize(700, 600)
    
    # Set window style with a modern look
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme
    
    # Configure colors
    bg_color = "#f5f9ff"
    accent_color = "#1e40af"
    secondary_color = "#059669"
    text_color = "#1e293b"
    card_bg = "#ffffff"
    
    root.configure(bg=bg_color)
    
    # Create header frame with gradient effect
    header_frame = tk.Frame(root, height=100, bg=accent_color)
    header_frame.pack(fill=tk.X)
    
    # Create logo and title frame
    logo_title_frame = tk.Frame(header_frame, bg=accent_color)
    logo_title_frame.pack(pady=15)
    
    # Load and display logo
    try:
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "商标.jfif")
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((70, 70), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        
        logo_label = tk.Label(logo_title_frame, image=logo_photo, bg=accent_color)
        logo_label.image = logo_photo  # Keep a reference to prevent garbage collection
        logo_label.pack(side=tk.LEFT, padx=10)
    except Exception as e:
        print(f"Error loading logo: {e}")
    
    # Create title and company name
    title_frame = tk.Frame(logo_title_frame, bg=accent_color)
    title_frame.pack(side=tk.LEFT, padx=15)
    
    title_label = tk.Label(
        title_frame, 
        text="PDF知识提取器", 
        font=("Microsoft YaHei", 26, "bold"),
        bg=accent_color,
        fg="white",
    )
    title_label.pack(anchor="w")
    
    company_label = tk.Label(
        title_frame, 
        text="北京风起时域科技有限公司", 
        font=("Microsoft YaHei", 12),
        bg=accent_color,
        fg="white",
    )
    company_label.pack(anchor="w", pady=(2, 0))
    
    # Create main content area with card-like appearance
    main_frame = tk.Frame(root, bg=bg_color)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
    
    # Create card frame
    card_frame = tk.Frame(
        main_frame, 
        bg=card_bg,
        highlightbackground="#e2e8f0",
        highlightthickness=1,
        bd=0
    )
    card_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Add inner padding to card
    inner_frame = tk.Frame(card_frame, bg=card_bg)
    inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Create info label with icon
    info_frame = tk.Frame(inner_frame, bg=card_bg)
    info_frame.pack(fill=tk.X, pady=10)
    
    info_icon = "ℹ️"  # Info emoji
    info_icon_label = tk.Label(
        info_frame,
        text=info_icon,
        font=("Microsoft YaHei", 16),
        bg=card_bg,
        fg=accent_color
    )
    info_icon_label.pack(side=tk.LEFT, padx=(0, 10))
    
    info_label = tk.Label(
        info_frame, 
        text="使用智谱AI分析PDF文档并提取关键知识点",
        font=("Microsoft YaHei", 12),
        bg=card_bg,
        fg=text_color,
        justify=tk.LEFT,
        wraplength=550
    )
    info_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Create horizontal separator
    separator = ttk.Separator(inner_frame, orient='horizontal')
    separator.pack(fill=tk.X, pady=15)
    
    # Create button frame
    button_frame = tk.Frame(inner_frame, bg=card_bg)
    button_frame.pack(pady=20)
    
    # Create select file button with hover effect
    def on_enter_file(e):
        select_file_button['background'] = '#047857'
        
    def on_leave_file(e):
        select_file_button['background'] = secondary_color
        
    def on_enter_folder(e):
        select_folder_button['background'] = '#1d4ed8'
        
    def on_leave_folder(e):
        select_folder_button['background'] = accent_color
    
    def on_enter_exit(e):
        exit_button['background'] = '#b91c1c'
        
    def on_leave_exit(e):
        exit_button['background'] = '#dc2626'
    
    # 选择并处理单个PDF文件
    def select_and_process_pdf():
        # Open file selection dialog
        pdf_path = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf")]
        )
        
        # If user cancels file selection, return
        if not pdf_path:
            return
        
        # Show processing message
        status_label.config(text="正在处理PDF文件，请稍候...")
        progress_bar.pack(pady=15)
        progress_bar.start(10)
        root.update()
        
        try:
            # Process PDF file
            api_key = os.getenv("ZHIPUAI_API_KEY")
            content = process_pdf(pdf_path, api_key, as_questions=True)
            
            # Save to markdown file
            output_path = save_to_markdown(content, pdf_path)
            
            # Stop progress bar
            progress_bar.stop()
            progress_bar.pack_forget()
            
            if output_path:
                status_label.config(text=f"分析完成！结果已保存至: {os.path.basename(output_path)}")
                messagebox.showinfo("处理完成", f"PDF分析结果已保存至:\n{output_path}")
            else:
                status_label.config(text="分析完成，但结果未保存")
        except Exception as e:
            progress_bar.stop()
            progress_bar.pack_forget()
            status_label.config(text=f"处理出错: {str(e)}")
            messagebox.showerror("处理错误", str(e))
            
    # 选择并处理整个文件夹的PDF文件
    def select_and_process_folder():
        # 打开文件夹选择对话框
        folder_path = filedialog.askdirectory(
            title="选择包含PDF文件的文件夹"
        )
        
        # 如果用户取消选择，返回
        if not folder_path:
            return
        
        # 显示处理消息
        status_label.config(text="正在处理文件夹中的PDF文件，请稍候...")
        progress_bar.pack(pady=15)
        progress_bar.start(10)
        root.update()
        
        try:
            # 处理文件夹
            api_key = os.getenv("ZHIPUAI_API_KEY")
            result = process_folder(folder_path, api_key, as_questions=True)
            
            # 停止进度条
            progress_bar.stop()
            progress_bar.pack_forget()
            
            if result["total_processed"] > 0:
                status_label.config(text=f"处理完成！成功处理 {result['total_processed']} 个文件，失败 {result['total_errors']} 个")
                messagebox.showinfo("处理完成", 
                                   f"成功处理 {result['total_processed']} 个PDF文件\n"
                                   f"失败 {result['total_errors']} 个\n\n"
                                   f"所有Markdown文件已保存在同一文件夹中")
            else:
                status_label.config(text="未处理任何文件")
                messagebox.showinfo("处理完成", "未处理任何文件")
        except Exception as e:
            progress_bar.stop()
            progress_bar.pack_forget()
            status_label.config(text=f"处理出错: {str(e)}")
            messagebox.showerror("处理错误", str(e))
            content = process_pdf(pdf_path, api_key)
            
            # Save results
            output_path = save_to_markdown(content, pdf_path)
            
            progress_bar.stop()
            progress_bar.pack_forget()
            
            if output_path:
                status_label.config(text=f"分析完成！结果已保存至: {os.path.basename(output_path)}")
                messagebox.showinfo("处理完成", f"PDF分析结果已保存至:\n{output_path}")
            else:
                status_label.config(text="分析完成，但结果未保存")
        except Exception as e:
            progress_bar.stop()
            progress_bar.pack_forget()
            status_label.config(text=f"处理出错: {str(e)}")
            messagebox.showerror("处理错误", str(e))
    
    select_file_button = tk.Button(
        button_frame,
        text="选择单个PDF文件",
        command=select_and_process_pdf,
        width=20,
        height=2,
        bg=secondary_color,
        fg="white",
        font=("Microsoft YaHei", 12, "bold"),
        relief=tk.FLAT,
        cursor="hand2",
        bd=0
    )
    select_file_button.pack(side=tk.LEFT, padx=10)
    select_file_button.bind("<Enter>", on_enter_file)
    select_file_button.bind("<Leave>", on_leave_file)
    
    select_folder_button = tk.Button(
        button_frame,
        text="选择PDF文件夹",
        command=select_and_process_folder,
        width=20,
        height=2,
        bg=accent_color,
        fg="white",
        font=("Microsoft YaHei", 12, "bold"),
        relief=tk.FLAT,
        cursor="hand2",
        bd=0
    )
    select_folder_button.pack(side=tk.LEFT, padx=10)
    select_folder_button.bind("<Enter>", on_enter_folder)
    select_folder_button.bind("<Leave>", on_leave_folder)
    
    # Create exit button
    exit_button = tk.Button(
        button_frame,
        text="退出程序",
        command=root.destroy,
        width=10,
        height=2,
        bg="#dc2626",
        fg="white",
        font=("Microsoft YaHei", 12, "bold"),
        relief=tk.FLAT,
        cursor="hand2",
        borderwidth=0
    )
    exit_button.pack(side=tk.LEFT, padx=10)
    exit_button.bind("<Enter>", on_enter_exit)
    exit_button.bind("<Leave>", on_leave_exit)
    
    # Create status frame
    status_frame = tk.Frame(inner_frame, bg=card_bg)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
    
    # Create progress bar with custom style (hidden by default)
    style.configure("TProgressbar", thickness=8, troughcolor="#e2e8f0", background=accent_color)
    progress_bar = ttk.Progressbar(status_frame, style="TProgressbar", mode='indeterminate', length=500)
    
    # Create status label
    status_label = tk.Label(
        status_frame, 
        text="准备就绪，请选择一个PDF文件",
        font=("Microsoft YaHei", 11),
        bg=card_bg,
        fg=text_color,
        pady=10
    )
    status_label.pack()
    
    # Create footer with copyright
    footer_frame = tk.Frame(root, bg=bg_color, height=30)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    copyright_label = tk.Label(
        footer_frame,
        text="© 2023 PDF Knowledge Summarizer - Powered by ZhipuAI",
        font=("Helvetica", 9),
        bg=bg_color,
        fg="#64748b"
    )
    copyright_label.pack(pady=5)
    
    # Run main loop
    root.mainloop()


def cli_mode():
    """
    Command Line Interface mode
    """
    # Load environment variables
    load_dotenv()
    
    # Create command line argument parser
    parser = argparse.ArgumentParser(description='Summarize PDF document content using ZhipuAI')
    parser.add_argument('pdf_path', nargs='?', help='PDF file path')
    parser.add_argument('--api-key', '-k', help='ZhipuAI API key, if not provided it will be retrieved from ZHIPU_API_KEY environment variable')
    parser.add_argument('--output', '-o', help='Output file path, if not provided output will be sent to console')
    parser.add_argument('--gui', '-g', action='store_true', help='Enable graphical user interface mode')
    
    # Parse command line arguments
    args = parser.parse_args()
    
    # If --gui parameter is specified or pdf_path is not provided, start GUI mode
    if args.gui or not args.pdf_path:
        gui_mode()
        return
    
    # Check if PDF file exists
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file does not exist: {args.pdf_path}")
        sys.exit(1)
    
    try:
        # Process PDF file
        output_content = process_pdf(args.pdf_path, args.api_key)
        
        # Output results
        if args.output:
            # Output to file
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_content)
            print(f"Summary saved to: {args.output}")
        else:
            # Output to console
            print("\n" + "="*50)
            print(output_content)
            print("="*50)
        
        print("Processing complete!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
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