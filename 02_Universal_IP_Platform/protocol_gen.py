import yaml
import os
from antigravity.sdk import Agent

def generate_protocol(config_path):
    # 1. 读取配置文件
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    meta = config['ip_元数据']
    
    # 2. 构造超级提示词 (注入多维 IP 特征)
    prompt = f"""
    你是一个顶级知识工程专家。请为 IP【{meta['姓名']}】所在的【{meta['领域']}】领域生成一套《知识原子化萃取协议》。
    
    [IP 深度画像]
    - 核心价值观：{', '.join(meta['核心价值观'])}
    - 语言风格：{meta['语言风格']}
    - 核心方法论：{meta['核心方法论']}
    - 目标受众：{meta['目标受众']}
    - 知识结构特征：{meta['知识结构体系']}
    - 性格设定：{meta['性格特征']}
    
    [萃取准则]
    1. 识别并提取该 IP 独特的“金句/关键词”：{meta['口头禅/金句标志']}。
    2. 针对【{meta['目标受众']}】的理解习惯，对【{meta['核心方法论']}】进行条理化提炼。
    3. 输出必须包含 [KB_ENTRY_START] 标签，并包含元数据、逻辑内核、及 1:1 无损还原的【金句区】。
    
    请产出一份不仅包含提取规则，还包含“如何模拟该 IP 语气”的深度协议 Markdown。
    """
    
    # 3. 调用 AI 生成协议
    print(f"正在为 {meta['姓名']} 炼制领域专用协议...")
    agent = Agent()
    response = agent.chat(prompt)
    
    # 4. 保存协议文件
    output_dir = os.path.join(os.path.dirname(__file__), "generated_protocols")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    protocol_filename = f"{meta['姓名']}_协议.md"
    protocol_path = os.path.join(output_dir, protocol_filename)
    
    with open(protocol_path, 'w', encoding='utf-8') as f:
        f.write(response.content)
        
    print(f"协议炼成成功：{protocol_path}")
    return protocol_path

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    config_file = os.path.join(base_dir, "ip_config_template.yaml")
    if os.path.exists(config_file):
        generate_protocol(config_file)
    else:
        print(f"找不到配置文件: {config_file}")
