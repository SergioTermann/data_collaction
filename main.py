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


def process_pdf(pdf_path, api_key=None):
    """
    Process PDF file and return results
    """
    try:
        # Initialize PDF summarizer
        summarizer = PDFSummarizer(api_key=api_key)
        
        # Summarize PDF content
        print(f"Processing PDF file: {pdf_path}")
        result = summarizer.summarize_pdf(pdf_path)
        
        # Format output content
        output_content = f"""
# PDF Document Summary

## File Information
- File: {os.path.basename(pdf_path)}
- Pages: {result['page_count']}
- Analysis Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Content Summary
{result['summary']}

## Key Concepts
{result['key_concepts']}
"""
        return output_content
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")


def save_to_markdown(content, pdf_path):
    """
    Save content to Markdown file
    """
    # Generate default output filename (based on original PDF filename)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    default_output = f"{base_name}_summary.md"
    
    # Open save file dialog
    output_path = filedialog.asksaveasfilename(
        defaultextension=".md",
        filetypes=[("Markdown Files", "*.md")],
        initialfile=default_output,
        title="Save Analysis Results"
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
    root.title("PDF Knowledge Summarizer")
    root.geometry("700x600")
    root.minsize(650, 550)
    
    # Set window style with a modern look
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme
    
    # Configure colors
    bg_color = "#f0f6fc"
    accent_color = "#2563eb"
    secondary_color = "#10b981"
    text_color = "#1e293b"
    card_bg = "#ffffff"
    
    root.configure(bg=bg_color)
    
    # Create header frame with gradient effect
    header_frame = tk.Frame(root, height=90, bg=accent_color)
    header_frame.pack(fill=tk.X)
    
    # Create logo and title frame
    logo_title_frame = tk.Frame(header_frame, bg=accent_color)
    logo_title_frame.pack(pady=10)
    
    # Load and display logo
    try:
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "商标.jfif")
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((60, 60), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        
        logo_label = tk.Label(logo_title_frame, image=logo_photo, bg=accent_color)
        logo_label.image = logo_photo  # Keep a reference to prevent garbage collection
        logo_label.pack(side=tk.LEFT, padx=10)
    except Exception as e:
        print(f"Error loading logo: {e}")
    
    # Create title label
    title_label = tk.Label(
        logo_title_frame, 
        text="PDF Knowledge Summarizer", 
        font=("Helvetica", 24, "bold"),
        bg=accent_color,
        fg="white",
    )
    title_label.pack(side=tk.LEFT, padx=15)
    
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
        font=("Helvetica", 16),
        bg=card_bg,
        fg=accent_color
    )
    info_icon_label.pack(side=tk.LEFT, padx=(0, 10))
    
    info_label = tk.Label(
        info_frame, 
        text="Analyze PDF documents and extract key knowledge points using ZhipuAI",
        font=("Helvetica", 12),
        bg=card_bg,
        fg=text_color,
        justify=tk.LEFT,
        wraplength=500
    )
    info_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Create horizontal separator
    separator = ttk.Separator(inner_frame, orient='horizontal')
    separator.pack(fill=tk.X, pady=15)
    
    # Create button frame
    button_frame = tk.Frame(inner_frame, bg=card_bg)
    button_frame.pack(pady=20)
    
    # Create select file button with hover effect
    def on_enter(e):
        select_button['background'] = '#0ea875'
        
    def on_leave(e):
        select_button['background'] = secondary_color
    
    def on_enter_exit(e):
        exit_button['background'] = '#e05252'
        
    def on_leave_exit(e):
        exit_button['background'] = '#e74c3c'
    
    # Create select file button
    def select_and_process_pdf():
        # Open file selection dialog
        pdf_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        # If user cancels file selection, return
        if not pdf_path:
            return
        
        # Show processing message
        status_label.config(text="Processing PDF file, please wait...")
        progress_bar.pack(pady=15)
        progress_bar.start(10)
        root.update()
        
        try:
            # Process PDF file
            api_key = "d2811fc4f03f48f2bb547d6a6b3378f4.GtaNMZOyqulNGa1L"
            content = process_pdf(pdf_path, api_key)
            
            # Save results
            output_path = save_to_markdown(content, pdf_path)
            
            progress_bar.stop()
            progress_bar.pack_forget()
            
            if output_path:
                status_label.config(text=f"Analysis complete! Results saved to: {os.path.basename(output_path)}")
                messagebox.showinfo("Processing Complete", f"PDF analysis results saved to:\n{output_path}")
            else:
                status_label.config(text="Analysis complete, but results were not saved")
        except Exception as e:
            progress_bar.stop()
            progress_bar.pack_forget()
            status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Processing Error", str(e))
    
    select_button = tk.Button(
        button_frame,
        text="Select PDF File",
        command=select_and_process_pdf,
        width=20,
        height=2,
        bg=secondary_color,
        fg="white",
        font=("Helvetica", 12, "bold"),
        relief=tk.FLAT,
        cursor="hand2",
        borderwidth=0
    )
    select_button.pack(side=tk.LEFT, padx=10)
    select_button.bind("<Enter>", on_enter)
    select_button.bind("<Leave>", on_leave)
    
    # Create exit button
    exit_button = tk.Button(
        button_frame,
        text="Exit",
        command=root.destroy,
        width=10,
        height=2,
        bg="#e74c3c",
        fg="white",
        font=("Helvetica", 12, "bold"),
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
        text="Ready. Please select a PDF file",
        font=("Helvetica", 11),
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