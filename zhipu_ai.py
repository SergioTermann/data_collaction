import os
from zai import ZhipuAiClient
from dotenv import load_dotenv

class ZhipuAI:
    def __init__(self, api_key=None):
        """
        初始化智谱AI客户端
        
        Args:
            api_key: 智谱AI的API密钥，如果为None则从环境变量获取
        """
        # 加载环境变量
        load_dotenv()
        
        # 获取API密钥
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        if not self.api_key:
            raise ValueError("未提供API密钥，请设置环境变量ZHIPU_API_KEY或在初始化时提供")
        
        # 初始化客户端
        self.client = ZhipuAiClient(api_key=self.api_key)
    
    def summarize_text(self, text, max_tokens=2000):
        """
        使用智谱AI总结文本内容
        
        Args:
            text: 需要总结的文本
            max_tokens: 输入文本的最大token数，默认2000
        
        Returns:
            str: 总结后的内容
        """
        # 如果文本过长，截取一部分
        if len(text) > max_tokens * 4:  # 粗略估计每个token约4个字符
            text = text[:max_tokens * 4]
            text += "\n[文本过长，已截断]"
        
        try:
            # 创建聊天完成请求
            response = self.client.chat.completions.create(
                model="glm-4.6",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的文档分析助手，擅长提取和总结文档中的关键知识点。请提取以下文本中的主要知识点，并按照重要性组织成结构化的总结。"
                    },
                    {
                        "role": "user",
                        "content": f"请总结以下PDF文档的主要内容，提取关键知识点，并按照重要性组织成结构化的总结：\n\n{text}"
                    }
                ],
                temperature=0.3  # 使用较低的温度以获得更确定性的回答
            )
            
            # 获取回复
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"调用智谱AI接口时出错: {str(e)}")
    
    def extract_key_concepts(self, text, max_tokens=2000):
        """
        使用智谱AI提取文本中的关键概念
        
        Args:
            text: 需要分析的文本
            max_tokens: 输入文本的最大token数，默认2000
        
        Returns:
            str: 提取的关键概念
        """
        # 如果文本过长，截取一部分
        if len(text) > max_tokens * 4:
            text = text[:max_tokens * 4]
            text += "\n[文本过长，已截断]"
        
        try:
            # 创建聊天完成请求
            response = self.client.chat.completions.create(
                model="glm-4.6",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的知识提取助手，擅长从文本中提取关键概念和术语。请从以下文本中提取关键概念，并简要解释每个概念。"
                    },
                    {
                        "role": "user",
                        "content": f"请从以下PDF文档中提取10-15个关键概念或术语，并为每个概念提供简短的解释：\n\n{text}"
                    }
                ],
                temperature=0.3
            )
            
            # 获取回复
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"调用智谱AI接口时出错: {str(e)}")