#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试文件 - 测试PDF处理和智谱AI功能
用于验证项目中各个API组件是否正常工作

使用方法:
    python test_api.py
    
或者运行特定测试:
    python test_api.py --test zhipu
    python test_api.py --test pdf
    python test_api.py --test all
"""

import os
import sys
import argparse
import time
from datetime import datetime
from dotenv import load_dotenv

# 导入项目模块
try:
    from zhipu_ai import ZhipuAI
    from pdf_reader import PDFReader
    from pdf_summarizer import PDFSummarizer
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保所有依赖模块都在当前目录中")
    sys.exit(1)


class APITester:
    """API测试类"""
    
    def __init__(self):
        """初始化测试器"""
        self.load_environment()
        self.test_results = {}
        self.start_time = None
        
    def load_environment(self):
        """加载环境变量"""
        load_dotenv()
        self.api_key = os.getenv("ZHIPU_API_KEY")
        
    def log(self, message, level="INFO"):
        """记录测试日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def test_environment(self):
        """测试环境配置"""
        self.log("🔧 测试环境配置...")
        
        results = {
            "env_file_exists": os.path.exists(".env"),
            "api_key_loaded": bool(self.api_key),
            "python_version": sys.version,
            "current_directory": os.getcwd()
        }
        
        if results["env_file_exists"]:
            self.log("✅ .env 文件存在")
        else:
            self.log("⚠️  .env 文件不存在", "WARNING")
            
        if results["api_key_loaded"]:
            self.log("✅ API密钥已加载")
        else:
            self.log("❌ API密钥未找到", "ERROR")
            
        self.log(f"📍 Python版本: {sys.version.split()[0]}")
        self.log(f"📁 当前目录: {os.getcwd()}")
        
        return results
        
    def test_zhipu_ai_connection(self):
        """测试智谱AI连接"""
        self.log("🤖 测试智谱AI连接...")
        
        if not self.api_key:
            self.log("❌ 无法测试智谱AI - API密钥未设置", "ERROR")
            return {"success": False, "error": "API密钥未设置"}
            
        try:
            # 初始化智谱AI客户端
            zhipu = ZhipuAI(self.api_key)
            self.log("✅ 智谱AI客户端初始化成功")
            
            # 测试简单的文本总结
            test_text = "这是一个测试文本。人工智能是计算机科学的一个分支，它试图理解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。"
            
            self.log("📝 测试文本总结功能...")
            start_time = time.time()
            summary = zhipu.summarize_text(test_text, max_tokens=100, as_questions=False)
            end_time = time.time()
            
            if summary and not summary.startswith("错误"):
                self.log("✅ 文本总结功能正常")
                self.log(f"⏱️  响应时间: {end_time - start_time:.2f}秒")
                self.log(f"📄 总结结果: {summary[:100]}...")
                
                # 测试关键概念提取
                self.log("🔍 测试关键概念提取...")
                start_time = time.time()
                concepts = zhipu.extract_key_concepts(test_text, max_tokens=100, as_questions=True)
                end_time = time.time()
                
                if concepts and not concepts.startswith("错误"):
                    self.log("✅ 关键概念提取功能正常")
                    self.log(f"⏱️  响应时间: {end_time - start_time:.2f}秒")
                    self.log(f"💡 概念结果: {concepts[:100]}...")
                    
                    return {
                        "success": True,
                        "summary": summary,
                        "concepts": concepts,
                        "response_time": end_time - start_time
                    }
                else:
                    self.log(f"❌ 关键概念提取失败: {concepts}", "ERROR")
                    return {"success": False, "error": f"关键概念提取失败: {concepts}"}
            else:
                self.log(f"❌ 文本总结失败: {summary}", "ERROR")
                return {"success": False, "error": f"文本总结失败: {summary}"}
                
        except Exception as e:
            self.log(f"❌ 智谱AI测试失败: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
            
    def test_pdf_reader(self):
        """测试PDF读取功能"""
        self.log("📚 测试PDF读取功能...")
        
        # 查找测试PDF文件
        test_pdf = None
        for file in os.listdir("."):
            if file.lower().endswith(".pdf"):
                test_pdf = file
                break
                
        if not test_pdf:
            self.log("⚠️  未找到PDF文件进行测试", "WARNING")
            return {"success": False, "error": "未找到PDF文件"}
            
        try:
            self.log(f"📖 使用文件: {test_pdf}")
            
            # 测试PDF读取
            pdf_reader = PDFReader(test_pdf)
            self.log("✅ PDF读取器初始化成功")
            
            # 获取页数
            page_count = pdf_reader.get_page_count()
            self.log(f"📄 PDF页数: {page_count}")
            
            # 读取内容
            start_time = time.time()
            content = pdf_reader.read_pdf()
            end_time = time.time()
            
            if content:
                content_length = len(content)
                self.log(f"✅ PDF内容读取成功")
                self.log(f"📊 内容长度: {content_length} 字符")
                self.log(f"⏱️  读取时间: {end_time - start_time:.2f}秒")
                self.log(f"📝 内容预览: {content[:200]}...")
                
                return {
                    "success": True,
                    "file": test_pdf,
                    "page_count": page_count,
                    "content_length": content_length,
                    "read_time": end_time - start_time,
                    "content_preview": content[:200]
                }
            else:
                self.log("❌ PDF内容为空", "ERROR")
                return {"success": False, "error": "PDF内容为空"}
                
        except Exception as e:
            self.log(f"❌ PDF读取测试失败: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
            
    def test_pdf_summarizer(self):
        """测试PDF摘要功能"""
        self.log("📋 测试PDF摘要功能...")
        
        if not self.api_key:
            self.log("❌ 无法测试PDF摘要 - API密钥未设置", "ERROR")
            return {"success": False, "error": "API密钥未设置"}
            
        # 查找测试PDF文件
        test_pdf = None
        for file in os.listdir("."):
            if file.lower().endswith(".pdf"):
                test_pdf = file
                break
                
        if not test_pdf:
            self.log("⚠️  未找到PDF文件进行测试", "WARNING")
            return {"success": False, "error": "未找到PDF文件"}
            
        try:
            self.log(f"📖 使用文件: {test_pdf}")
            
            # 初始化PDF摘要器
            summarizer = PDFSummarizer(self.api_key)
            self.log("✅ PDF摘要器初始化成功")
            
            # 执行摘要
            self.log("🔄 开始生成摘要...")
            start_time = time.time()
            result = summarizer.summarize_pdf(test_pdf, as_questions=True)
            end_time = time.time()
            
            if result and "summary" in result and "key_concepts" in result:
                self.log("✅ PDF摘要生成成功")
                self.log(f"⏱️  处理时间: {end_time - start_time:.2f}秒")
                self.log(f"📄 页数: {result.get('page_count', 'N/A')}")
                self.log(f"📝 摘要长度: {len(result['summary'])} 字符")
                self.log(f"💡 概念长度: {len(result['key_concepts'])} 字符")
                self.log(f"📋 摘要预览: {result['summary'][:200]}...")
                
                return {
                    "success": True,
                    "file": test_pdf,
                    "processing_time": end_time - start_time,
                    "page_count": result.get('page_count'),
                    "summary_length": len(result['summary']),
                    "concepts_length": len(result['key_concepts']),
                    "summary_preview": result['summary'][:200]
                }
            else:
                self.log("❌ PDF摘要生成失败", "ERROR")
                return {"success": False, "error": "摘要生成失败"}
                
        except Exception as e:
            self.log(f"❌ PDF摘要测试失败: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
            
    def test_error_handling(self):
        """测试错误处理"""
        self.log("🛡️  测试错误处理...")
        
        error_tests = {}
        
        # 测试无效API密钥
        try:
            invalid_zhipu = ZhipuAI("invalid_key")
            result = invalid_zhipu.summarize_text("测试文本")
            if result.startswith("错误"):
                error_tests["invalid_api_key"] = "✅ 正确处理无效API密钥"
            else:
                error_tests["invalid_api_key"] = "❌ 未正确处理无效API密钥"
        except Exception:
            error_tests["invalid_api_key"] = "✅ 正确抛出异常处理无效API密钥"
            
        # 测试不存在的PDF文件
        try:
            pdf_reader = PDFReader("nonexistent.pdf")
            content = pdf_reader.read_pdf()
            error_tests["nonexistent_pdf"] = "❌ 未正确处理不存在的PDF文件"
        except Exception:
            error_tests["nonexistent_pdf"] = "✅ 正确处理不存在的PDF文件"
            
        # 测试空API密钥
        try:
            empty_zhipu = ZhipuAI("")
            error_tests["empty_api_key"] = "❌ 未正确处理空API密钥"
        except ValueError:
            error_tests["empty_api_key"] = "✅ 正确处理空API密钥"
        except Exception:
            error_tests["empty_api_key"] = "⚠️  处理空API密钥但异常类型不符"
            
        for test_name, result in error_tests.items():
            self.log(f"{result}")
            
        return error_tests
        
    def run_all_tests(self):
        """运行所有测试"""
        self.start_time = time.time()
        self.log("🚀 开始API测试...")
        self.log("=" * 50)
        
        # 环境测试
        self.test_results["environment"] = self.test_environment()
        self.log("-" * 30)
        
        # 智谱AI测试
        self.test_results["zhipu_ai"] = self.test_zhipu_ai_connection()
        self.log("-" * 30)
        
        # PDF读取测试
        self.test_results["pdf_reader"] = self.test_pdf_reader()
        self.log("-" * 30)
        
        # PDF摘要测试
        self.test_results["pdf_summarizer"] = self.test_pdf_summarizer()
        self.log("-" * 30)
        
        # 错误处理测试
        self.test_results["error_handling"] = self.test_error_handling()
        self.log("-" * 30)
        
        # 生成测试报告
        self.generate_report()
        
    def generate_report(self):
        """生成测试报告"""
        end_time = time.time()
        total_time = end_time - self.start_time
        
        self.log("📊 测试报告")
        self.log("=" * 50)
        
        success_count = 0
        total_count = 0
        
        for test_name, result in self.test_results.items():
            if test_name == "error_handling":
                continue  # 错误处理测试单独计算
                
            total_count += 1
            if isinstance(result, dict) and result.get("success", False):
                success_count += 1
                self.log(f"✅ {test_name}: 通过")
            else:
                self.log(f"❌ {test_name}: 失败")
                if isinstance(result, dict) and "error" in result:
                    self.log(f"   错误: {result['error']}")
                    
        self.log(f"📈 测试通过率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
        self.log(f"⏱️  总测试时间: {total_time:.2f}秒")
        
        # 建议
        self.log("\n💡 建议:")
        if not self.test_results["environment"].get("api_key_loaded"):
            self.log("   - 请在.env文件中设置ZHIPU_API_KEY")
        if not self.test_results["pdf_reader"].get("success"):
            self.log("   - 请在项目目录中放置PDF文件进行测试")
        if success_count == total_count:
            self.log("   - 所有测试通过！API功能正常 🎉")
            
        self.log("=" * 50)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="API测试工具")
    parser.add_argument("--test", choices=["env", "zhipu", "pdf", "summarizer", "error", "all"], 
                       default="all", help="选择要运行的测试")
    
    args = parser.parse_args()
    
    tester = APITester()
    
    if args.test == "all":
        tester.run_all_tests()
    elif args.test == "env":
        tester.test_environment()
    elif args.test == "zhipu":
        tester.test_zhipu_ai_connection()
    elif args.test == "pdf":
        tester.test_pdf_reader()
    elif args.test == "summarizer":
        tester.test_pdf_summarizer()
    elif args.test == "error":
        tester.test_error_handling()


if __name__ == "__main__":
    main()