import os
import yaml
from antigravity.sdk import Agent

class IPFactoryCore:
    def __init__(self, config_path, protocol_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.meta = self.config['ip_元数据']
        self.rules = self.config['萃取规则']
        self.protocol_path = protocol_path
        
        # 路径标准化：默认在平台文件夹下的 output_kb
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.output_base = os.path.join(base_dir, "output_assets")
        self.ip_output_dir = os.path.join(self.output_base, self.meta['姓名'])
        
        if not os.path.exists(self.ip_output_dir):
            os.makedirs(self.ip_output_dir)
            
        self.agent = Agent(system_prompt_ref=self.protocol_path)

    def process_file(self, file_path):
        filename = os.path.basename(file_path)
        print(f"🚀 核心引擎启动：正在深度提炼 {filename}...")
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
            
        # 动态分片：根据配置调整
        chunk_size = self.rules.get('最小分片字数', 8000)
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        result_content = ""
        for i, chunk in enumerate(chunks):
            print(f"   [进度] 处理第 {i+1}/{len(chunks)} 分片...")
            response = self.agent.chat(f"处理文档【{filename}】的第 {i+1} 部分：\n\n{chunk}")
            result_content += response.content + "\n\n---\n\n"
            
        save_name = filename.replace(".txt", "_Atomic.md")
        save_path = os.path.join(self.ip_output_dir, save_name)
        
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(result_content)
            
        print(f"✅ 提炼完成，资产已存入: {save_path}")

    def generate_index(self):
        print("📊 正在聚合全局知识映射 (MASTER_INDEX)...")
        all_files = [f for f in os.listdir(self.ip_output_dir) if f.endswith('.md') and f != "MASTER_INDEX.md"]
        file_list_str = "\n".join(all_files)
        
        index_prompt = f"请阅读以下萃取出的知识库文件名列表，为 IP【{self.meta['姓名']}】生成一份分模块的 MASTER_INDEX.md 文件。要求包含功能模块分类、文件链接和核心价值简述：\n{file_list_str}"
        index_res = self.agent.chat(index_prompt)
        
        index_path = os.path.join(self.ip_output_dir, "MASTER_INDEX.md")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_res.content)
        print(f"✨ 全局索引生成成功: {index_path}")

def run_full_pipeline(config_name="ip_config_template.yaml", input_dir_name="cleaned_text"):
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, config_name)
    
    # 自动定位协议文件 (逻辑：假设已经生成)
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    protocol_path = os.path.join(base_dir, "generated_protocols", f"{config['ip_元数据']['姓名']}_协议.md")
    
    input_dir = os.path.join(base_dir, input_dir_name)
    
    if not os.path.exists(protocol_path):
        print(f"❌ 错误：找不到协议文件 {protocol_path}，请先运行 protocol_gen.py")
        return

    factory = IPFactoryCore(config_path, protocol_path)
    
    if not os.path.exists(input_dir):
        print(f"❌ 错误：输入目录 {input_dir} 不存在")
        return
        
    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    for f in files:
        factory.process_file(os.path.join(input_dir, f))
        
    factory.generate_index()
    
    # [新增] 只有在工厂流水线跑完后，自动生成人格手册
    print("\n------------------------------")
    print("🎭 正在唤醒 IP 数字灵魂...")
    try:
        from persona_gen import generate_persona_manual
        generate_persona_manual(config_path)
    except Exception as e:
        print(f"⚠️ 人格手册生成失败: {e}")

if __name__ == "__main__":
    run_full_pipeline()
