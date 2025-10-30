import PyPDF2
import os

class PDFReader:
    def __init__(self, file_path):
        """
        初始化PDF读取器
        
        Args:
            file_path: PDF文件路径
        """
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF文件不存在: {file_path}")
        
        if not file_path.lower().endswith('.pdf'):
            raise ValueError(f"文件不是PDF格式: {file_path}")
    
    def read_pdf(self):
        """
        读取PDF文件内容
        
        Returns:
            str: PDF文件的文本内容
        """
        try:
            with open(self.file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                
                # 读取每一页内容
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text()
                
                return text
        except Exception as e:
            raise Exception(f"读取PDF文件时出错: {str(e)}")
    
    def get_page_count(self):
        """
        获取PDF文件页数
        
        Returns:
            int: PDF文件的页数
        """
        try:
            with open(self.file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return len(reader.pages)
        except Exception as e:
            raise Exception(f"获取PDF页数时出错: {str(e)}")