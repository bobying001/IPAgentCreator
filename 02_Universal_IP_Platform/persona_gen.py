import yaml
import os
from antigravity.sdk import Agent

def generate_persona_manual(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    meta = config['ip_元数据']
    output_base = config['萃取规则'].get('输出资产文件夹', "../output_assets")
    ip_output_dir = os.path.join(output_base, meta['姓名'])
    
    if not os.path.exists(ip_output_dir):
        os.makedirs(ip_output_dir)

    print(f"🧬 正在为 {meta['姓名']} 注入数字灵魂 (生成实操手册)...")
    
    agent = Agent()
    prompt = f"""
    你是一个数字人架构师。请基于以下 IP 画像，按照《李中莹IP数字化人格实操手册》的标准结构，为 AI 撰写一份用于角色扮演的系统级指令（System Instruction）。

    IP 深度画像：
    - 姓名：{meta['姓名']}
    - 领域：{meta['领域']}
    - 核心价值观：{', '.join(meta['核心价值观'])}
    - 语言风格：{meta['语言风格']}
    - 核心方法论：{meta['核心方法论']}
    - 目标受众：{meta['目标受众']}
    - 性格特征：{meta['性格特征']}

    生成的文档结构必须包含：
    # {meta['姓名']}：IP 数字化人格实操手册

    ## 1. 角色核心设定
    （定义你是谁，你的终极使命，你的伦理边界）

    ## 2. 语言与对话风格
    （包含具体的口癖、常用隐喻、禁忌词汇、语气强弱）

    ## 3. 认知思维框架（Thinking Framework）
    （定义当用户提出问题时，你应该调用的底层分析模型。例如NLP用BVR模型，投资用价值分析模型）

    ## 4. 交互行为规范
    - **倾听阶段**：如何通过提问澄清需求？
    - **回应阶段**：先讲原理还是先讲技巧？
    - **结束阶段**：如何像本人一样进行总结？

    ## 5. 知识库调用策略
    （指导 AI 何时引用 atomic 知识库中的定义和案例）
    
    这不仅仅是一份介绍，而是直接给 LLM 看的 "Instruction Prompt"。请用第二人称 "你" 来撰写。
    """
    
    response = agent.chat(prompt)
    
    filename = f"{meta['姓名']}_IP数字化人格实操手册.md"
    save_path = os.path.join(ip_output_dir, filename)
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(response.content)
        
    print(f"SUCCESS: 数字人格手册已生成 -> {save_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    config_file = os.path.join(base_dir, "ip_config_template.yaml")
    
    if os.path.exists(config_file):
        generate_persona_manual(config_file)
    else:
        print("请先配置 ip_config_template.yaml")
