import re
import os
import yaml

class DataCleaner:
    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.blacklist = config['系统自动生成项'].get('blacklist_patterns', [])

    def clean_text(self, text):
        # 1. 移除黑名单整行（根据配置自动生成的各平台特征）
        for word in self.blacklist:
            # 兼容正则和普通字符串
            text = re.sub(rf".*?{word}.*?\n", '', text, flags=re.IGNORECASE)
        
        # 2. 移除连续的特殊字符 (多用于装饰线条)
        text = re.sub(r'[-=＿—*]{5,}', '\n', text)
        
        # 3. 移除页码及页眉干扰 (通用正则)
        text = re.sub(r'(第\s*\d+\s*页|Page\s*\d+|·\d+·)', '', text, flags=re.IGNORECASE)
        
        # 4. 规范空行（最多连续两行）
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()

    def process(self, input_dir="raw_data", output_dir="cleaned_text"):
        base_dir = os.path.dirname(__file__)
        abs_input = os.path.join(base_dir, input_dir)
        abs_output = os.path.join(base_dir, output_dir)
        
        if not os.path.exists(abs_output):
            os.makedirs(abs_output)
            
        files = [f for f in os.listdir(abs_input) if f.endswith('.txt')]
        print(f"🧹 启动洗地程序，共计 {len(files)} 个文件...")
        
        for filename in files:
            with open(os.path.join(abs_input, filename), 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            cleaned = self.clean_text(content)
            
            with open(os.path.join(abs_output, filename), 'w', encoding='utf-8') as f:
                f.write(cleaned)
            print(f"   [完成] {filename}")

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    cleaner = DataCleaner(os.path.join(base_dir, "ip_config_template.yaml"))
    
    raw_path = os.path.join(base_dir, "raw_text")
    if os.path.exists(raw_path):
        cleaner.process("raw_text", "cleaned_text")
    else:
        print(f"💡 请将文本文件放入 {raw_path} 后再运行清洗。")
