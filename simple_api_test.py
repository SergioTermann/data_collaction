#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的智谱AI API测试
用于快速验证API连接是否正常
"""

import os
from dotenv import load_dotenv
import zhipuai

def test_zhipu_api():
    """测试智谱AI API连接"""
    print("🚀 开始测试智谱AI API连接...")
    
    # 加载环境变量
    load_dotenv()
    api_key = '95cb284c7c72414a97614176ff9be950.TAHocHfLFNXzB9Aq'
    
    if not api_key:
        print("❌ 错误: 未找到API密钥")
        print("请在.env文件中设置 ZHIPU_API_KEY=你的密钥")
        return False
    
    print(f"✅ API密钥已加载: {api_key[:10]}...")
    
    try:
        # 初始化客户端
        client = zhipuai.ZhipuAI(api_key=api_key)
        print("✅ 智谱AI客户端初始化成功")
        
        # 发送测试请求
        print("📤 发送测试请求...")
        
        response = client.chat.completions.create(
            model="glm-4.5",  # 使用GLM-4模型
            messages=[
                {"role": "user", "content": "你好，请简单介绍一下你自己"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        if response and response.choices:
            content = response.choices[0].message.content
            print("✅ API调用成功!")
            print(f"📝 响应内容: {content}")
            print(f"📊 使用的模型: {response.model}")
            print(f"🔢 消耗token: {response.usage.total_tokens if response.usage else '未知'}")
            return True
        else:
            print("❌ API调用失败: 未收到有效响应")
            return False
            
    except Exception as e:
        print(f"❌ API调用出错: {str(e)}")
        return False

def test_simple_chat():
    """测试简单对话功能"""
    print("\n🤖 测试简单对话功能...")
    
    load_dotenv()
    api_key = os.getenv("ZHIPU_API_KEY")
    
    if not api_key:
        print("❌ 跳过对话测试: 未找到API密钥")
        return False
    
    try:
        client = zhipuai.ZhipuAI(api_key=api_key)
        
        # 测试几个简单问题
        test_questions = [
            "1+1等于几？",
            "请用一句话解释什么是人工智能",
            "今天天气怎么样？"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n📝 问题{i}: {question}")
            
            response = client.chat.completions.create(
                model="glm-4",
                messages=[{"role": "user", "content": question}],
                max_tokens=50,
                temperature=0.7
            )
            
            if response and response.choices:
                answer = response.choices[0].message.content
                print(f"💬 回答: {answer}")
            else:
                print("❌ 未收到回答")
                
        return True
        
    except Exception as e:
        print(f"❌ 对话测试出错: {str(e)}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("🧪 智谱AI API 连接测试")
    print("=" * 50)
    
    # 基础连接测试
    basic_test = test_zhipu_api()
    
    if basic_test:
        # 如果基础测试通过，进行对话测试
        chat_test = test_simple_chat()
        
        print("\n" + "=" * 50)
        print("📊 测试结果汇总:")
        print(f"✅ 基础连接测试: {'通过' if basic_test else '失败'}")
        print(f"✅ 对话功能测试: {'通过' if chat_test else '失败'}")
        
        if basic_test and chat_test:
            print("🎉 恭喜! 智谱AI API连接完全正常!")
        else:
            print("⚠️  部分功能存在问题，请检查配置")
    else:
        print("\n❌ 基础连接测试失败，跳过其他测试")
        print("💡 请检查:")
        print("   1. .env文件是否存在")
        print("   2. ZHIPU_API_KEY是否正确设置")
        print("   3. 网络连接是否正常")
        print("   4. API密钥是否有效且有余额")
    
    print("=" * 50)


if __name__ == "__main__":
    main()