from pdf_reader import PDFReader
from zhipu_ai import ZhipuAI

class PDFSummarizer:
    def __init__(self, api_key=None):
        """
        初始化PDF总结器
        
        Args:
            api_key: 智谱AI的API密钥，如果为None则从环境变量获取
        """
        self.zhipu_ai = ZhipuAI(api_key)
    
    def summarize_pdf(self, pdf_path, as_questions=True, custom_instruction=None):
        """
        总结PDF文件内容
        
        Args:
            pdf_path: PDF文件路径
            as_questions: 如果为True，尽可能将内容格式化为问题形式
            custom_instruction: 用户自定义处理说明
        
        Returns:
            dict: 包含总结和关键概念的字典
        """
        # 读取PDF文件
        pdf_reader = PDFReader(pdf_path)
        text = pdf_reader.read_pdf()
        page_count = pdf_reader.get_page_count()
        
        print(f"成功读取PDF文件，共{page_count}页")
        
        # 总结内容
        print("正在使用智谱AI总结内容...")
        summary = self.zhipu_ai.summarize_text(text, as_questions=as_questions, custom_instruction=custom_instruction)
        
        # 提取关键概念
        print("正在提取关键概念...")
        key_concepts = self.zhipu_ai.extract_key_concepts(text, as_questions=as_questions, custom_instruction=custom_instruction)
        
        return {
            "summary": summary,
            "key_concepts": key_concepts,
            "page_count": page_count
        }