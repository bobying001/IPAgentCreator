import os
import sys

# 确保可以导入同目录下的模块
sys.path.append(os.path.dirname(__file__))

from extractor import run_extractor
from config_generator import generate_config
from cleaner import DataCleaner
from protocol_gen import generate_protocol
from factory_core import run_full_pipeline

def start_ip_factory():
    base_dir = os.path.dirname(__file__)
    
    print("====================================================")
    print("🚀  通用 IP 数字化工厂 - 全自动化流水线启动")
    print("====================================================\n")

    # Step 1: 格式转换 (PDF/Docx -> TXT)
    print("Step 1: 正在从 source_documents 提取原始文字...")
    run_extractor()
    
    # Step 2: AI 自动画像与配置生成
    raw_text_dir = os.path.join(base_dir, "raw_text")
    print("\nStep 2: 正在扫描语料并自动生成 IP 配置文件...")
    generate_config(raw_text_dir)
    
    # Step 3: 根据黑名单库自动洗地
    config_path = os.path.join(base_dir, "ip_config_template.yaml")
    print("\nStep 4: 正在根据识别出的平台特征清洗数据...")
    cleaner = DataCleaner(config_path)
    cleaner.process("raw_text", "cleaned_text")
    
    # Step 4: 炼制领域专用萃取协议
    print("\nStep 5: 正在炼制 AI 领域萃取协议 (System Prompt)...")
    generate_protocol(config_path)
    
    # Step 5: 开启核心萃取引擎 (产生 Atomic.md, MASTER_INDEX.md 和 Persona_Manual.md)
    print("\nStep 6: 启动核心炼成阵 - 生产数字化资产...")
    run_full_pipeline()

    print("\n====================================================")
    print("🎉  完工！请在 [output_assets] 文件夹中查收您的数字分身资产包。")
    print("====================================================")

if __name__ == "__main__":
    start_ip_factory()
