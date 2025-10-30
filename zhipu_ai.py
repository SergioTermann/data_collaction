import os
import zhipuai
from dotenv import load_dotenv

class ZhipuAI:
    def __init__(self, api_key=None):
        """
        Initialize ZhipuAI client
        
        Args:
            api_key: ZhipuAI API key, if None, get from environment variable
        """
        # Load environment variables
        load_dotenv()
        
        # Get API key
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided, please set ZHIPU_API_KEY environment variable or provide it during initialization")
        
        # Initialize client
        self.client = zhipuai.ZhipuAI(api_key=self.api_key)
    
    def summarize_text(self, text, max_tokens=2000):
        """
        Summarize text using ZhipuAI
        
        Args:
            text: Text to summarize
            max_tokens: Maximum tokens for the response
            
        Returns:
            Summary of the text
        """
        # Truncate text if too long
        if len(text) > max_tokens * 4:  # Rough estimate of 4 chars per token
            text = text[:max_tokens * 4]
            text += "\n[Text truncated due to length]"
        
        try:
            response = self.client.chat.completions.create(
                model="chatglm_turbo",
                messages=[
                    {"role": "system", "content": "You are a professional document analysis assistant, skilled at extracting and summarizing key knowledge points from documents."}, 
                    {"role": "user", "content": f"Please summarize the following document content, extract key points, and organize them into a structured summary:\n\n{text}"}
                ],
                top_p=0.7,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in summarize_text: {e}")
            return f"Error: {str(e)}"
    
    def extract_key_concepts(self, text, max_tokens=2000):
        """
        Extract key concepts from text using ZhipuAI
        
        Args:
            text: Text to extract key concepts from
            max_tokens: Maximum tokens for the response
            
        Returns:
            Key concepts extracted from the text
        """
        # Truncate text if too long
        if len(text) > max_tokens * 4:
            text = text[:max_tokens * 4]
            text += "\n[Text truncated due to length]"
        
        try:
            response = self.client.chat.completions.create(
                model="chatglm_turbo",
                messages=[
                    {"role": "system", "content": "You are a professional knowledge extraction assistant, skilled at extracting key concepts and terms from text."}, 
                    {"role": "user", "content": f"Please extract 10-15 key concepts or terms from the following document, and provide a brief explanation for each concept:\n\n{text}"}
                ],
                top_p=0.7,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in extract_key_concepts: {e}")
            return f"Error: {str(e)}"