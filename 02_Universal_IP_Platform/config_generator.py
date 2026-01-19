import os
import yaml
from antigravity.sdk import Agent

PLATFORM_BLACKS = {
    "WeChat": [
        "阅读原文", "扫描二维码", "往期回顾", "点击关注", "公众号", "点赞", "在看", "转发", 
        "未经授权禁止转载", "封面来源", "排版", "编辑", "作者简介"
    ],
    "LittleRedBook": [
        "笔记", "薯队长", "笔记灵感", "种草", "链接在评论区", "收藏", "点击头像", "小红书",
        "私人号", "合作请私信"
    ],
    "Zhihu": [
        "谢邀", "利益相关", "匿名用户", "以上", "知乎", "收藏夹吃灰", "赞同"
    ],
    "Book_Scan": [
        "第\s*\d+\s*页", "Page\s*\d+", "\d+", "■", "●", "★", "©", "ISBN"
    ]
}

def generate_config(raw_text_dir):
    # 1. 获取样本数据
    txt_files = [f for f in os.listdir(raw_text_dir) if f.endswith('.txt')]
    if not txt_files:
        print("❌ 错误：在 raw_text 中找不到 TXT 文件，请先运行 extractor.py。")
        return

    sample_text = ""
    # 从前 3 个文件中各抽取 2000 字作为样本
    for f in txt_files[:3]:
        with open(os.path.join(raw_text_dir, f), 'r', encoding='utf-8') as file:
            sample_text += file.read(2000) + "\n"

    # 2. 调用 AI 进行 IP 属性透视
    print("🧠 正在深度扫描语料，透视 IP 数字化特征...")
    agent = Agent()
    prompt = f"""
    你是一个 IP 扫描专家。请深度阅读以下语料样本，并根据内容还原出该博主/专家的数字化特征。
    请直接以 YAML 格式输出，包含以下字段：
    姓名、领域、核心价值观(list)、语言风格(描述)、核心方法论(具体名称)、目标受众、口头禅/金句标志、知识结构体系(理论为主/技巧为主/案例为主)、性格特征、建议的 platform(从 WeChat, LittleRedBook, Zhihu, Book_Scan 中选一)。

    语料样本：
    {sample_text}
    """
    
    response = agent.chat(prompt)
    
    # 3. 解析 AI 返回的 YAML
    try:
        # 去掉 Markdown 格式标记
        clean_response = response.content.replace("```yaml", "").replace("```", "").strip()
        ai_meta = yaml.safe_load(clean_response)
    except Exception as e:
        print(f"⚠️ AI 返回格式解析失败，将使用基础模板。错误: {e}")
        ai_meta = {}

    # 4. 构建最终配置文件内容
    platform = ai_meta.get('platform', 'WeChat')
    blacklist = PLATFORM_BLACKS.get(platform, [])

    final_config = {
        "ip_元数据": {
            "姓名": ai_meta.get('姓名', '未知'),
            "领域": ai_meta.get('领域', '未知'),
            "核心价值观": ai_meta.get('核心价值观', []),
            "语言风格": ai_meta.get('语言风格', '未知'),
            "核心方法论": ai_meta.get('核心方法论', '未知'),
            "目标受众": ai_meta.get('目标受众', '未知'),
            "口头禅/金句标志": ai_meta.get('口头禅/金句标志', '无'),
            "知识结构体系": ai_meta.get('知识结构体系', '理论主导'),
            "性格特征": ai_meta.get('性格特征', '未知')
        },
        "数据来源平台": {
            "platform": platform
        },
        "萃取增强配置": {
            "protocol_version": "2.0",
            "extract_cases": True,
            "min_chunk_size": 8000
        },
        "系统自动生成项": {
            "blacklist_patterns": blacklist,
            "domain_specific_keywords": []
        }
    }

    # 5. 保存配置文件
    config_path = os.path.join(os.path.dirname(__file__), "ip_config_template.yaml")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(final_config, f, allow_unicode=True, sort_keys=False)
    
    print(f"✨ IP 数字化配置文件已自动生成：{config_path}")
    print(f"💡 系统自动识别 IP 姓名为：【{final_config['ip_元数据']['姓名']}】")
    print(f"💡 系统根据内容自动匹配黑名单库为：【{platform}】")

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    raw_dir = os.path.join(base_dir, "raw_text")
    generate_config(raw_dir)
