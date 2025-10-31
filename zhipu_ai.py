import os
import zhipuai
from dotenv import load_dotenv

class ZhipuAI:
    def __init__(self, api_key=None):
        """
        初始化智谱AI客户端
        
        参数:
            api_key: 智谱AI的API密钥，如果为None，则从环境变量获取
        """
        # 加载环境变量
        load_dotenv()
        
        # 获取API密钥
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        if not self.api_key:
            raise ValueError("未提供API密钥，请设置ZHIPU_API_KEY环境变量或在初始化时提供")
        
        # 初始化客户端
        self.client = zhipuai.ZhipuAI(api_key=self.api_key)
    
    def summarize_text(self, text, max_tokens=2000, as_questions=True):
        """
        使用智谱AI总结文本
        
        参数:
            text: 要总结的文本
            max_tokens: 响应的最大令牌数
            as_questions: 如果为True，尽可能将内容格式化为问题形式
            
        返回:
            文本的总结
        """
        # 如果文本太长，进行截断
        if len(text) > max_tokens * 4:  # 粗略估计每个令牌4个字符
            text = text[:max_tokens * 4]
            text += "\n[文本因长度过长而被截断]"
        
        try:
            system_prompt = "你是一位专业的文档分析助手，擅长从文档中提取和总结关键知识点。请只使用中文回答。"
            
            if as_questions:
                user_prompt = f"请总结以下文档内容。对于可以表述为问题的概念，请以问题形式呈现。对于无法自然地表述为问题的内容，请使用正常的描述性格式。将所有内容组织成结构清晰的总结，并分为明确的部分。请确保所有输出都是中文，不要使用任何英文：\n\n{text}"
            else:
                user_prompt = f"请总结以下文档内容，提取关键点，并将它们组织成结构化的总结。请确保所有输出都是中文，不要使用任何英文：\n\n{text}"
            
            response = self.client.chat.completions.create(
                model="glm-4.6",
                messages=[
                    {"role": "system", "content": system_prompt}, 
                    {"role": "user", "content": user_prompt}
                ],
                top_p=0.7,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"总结文本时出错: {e}")
            return f"错误: {str(e)}"
    
    def extract_key_concepts(self, text, max_tokens=2000, as_questions=True):
        """
        从文本中提取关键概念
        
        参数:
            text: 要提取关键概念的文本
            max_tokens: 响应的最大令牌数
            as_questions: 如果为True，尽可能将概念格式化为问题形式
            
        返回:
            从文本中提取的关键概念
        """
        # 如果文本太长，进行截断
        if len(text) > max_tokens * 4:
            text = text[:max_tokens * 4]
            text += "\n[文本因长度过长而被截断]"
        
        try:
            system_prompt = "你是一位专业的知识提取助手，擅长从文本中提取关键概念和术语。请只使用中文回答。"
            
            if as_questions:
                user_prompt = f"请从以下文档中提取10-15个关键概念或术语。对于可以表述为问题的概念，请以问题形式呈现。对于无法自然地表述为问题的概念，请使用正常的描述性格式。为每个概念提供简要解释。请确保所有输出都是中文，不要使用任何英文：\n\n{text}"
            else:
                user_prompt = f"请从以下文档中提取10-15个关键概念或术语，并为每个概念提供简要解释。请确保所有输出都是中文，不要使用任何英文：\n\n{text}"
            
            response = self.client.chat.completions.create(
                model="glm-4.6",
                messages=[
                    {"role": "system", "content": system_prompt}, 
                    {"role": "user", "content": user_prompt}
                ],
                top_p=0.7,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"提取关键概念时出错: {e}")
            return f"错误: {str(e)}"