import os
from antigravity.sdk import Agent, FileSystem

# 配置参数
DOCS_PATH = "./documents"   # 请确保您的19个文档在这个文件夹里
OUTPUT_PATH = "./output_kb"
PROMPT_NAME = "NLP_Protocol.md"

def main():
    # 初始化环境
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    
    agent = Agent(system_prompt_ref=PROMPT_NAME)
    files = [f for f in os.listdir(DOCS_PATH) if f.endswith('.pdf')]
    
    print(f"找到 {len(files)} 个文档，启动李中莹知识萃取引擎...")

    for filename in files:
        full_path = os.path.join(DOCS_PATH, filename)
        print(f"正在深度解析: {filename}...")
        
        # 读取内容
        text = FileSystem.read_pdf(full_path)
        
        # 分片处理以保证无损提取（每片约1万字）
        chunks = [text[i:i+10000] for i in range(0, len(text), 10000)]
        
        result_content = ""
        for i, chunk in enumerate(chunks):
            response = agent.chat(f"处理文档【{filename}】的第 {i+1} 部分：\n\n{chunk}")
            result_content += response.content + "\n\n---\n\n"
        
        # 写入文件
        save_name = filename.replace(".pdf", "_Atomic.md")
        with open(os.path.join(OUTPUT_PATH, save_name), "w", encoding="utf-8") as f:
            f.write(result_content)
        print(f"解析完成，已存入: {save_name}")

    # 生成全局索引
    generate_index(agent)

def generate_index(agent):
    print("正在聚合知识库索引...")
    all_files = os.listdir(OUTPUT_PATH)
    file_list_str = "\n".join(all_files)
    
    index_prompt = f"请阅读以下萃取出的知识库文件名列表，生成一份按 NLP 模块（如：情绪、技巧、心法等）分类的 MASTER_INDEX.md 索引文件：\n{file_list_str}"
    index_res = agent.chat(index_prompt)
    
    with open(os.path.join(OUTPUT_PATH, "MASTER_INDEX.md"), "w", encoding="utf-8") as f:
        f.write(index_res.content)
    print("【全部任务已完成】请检查 output_kb 文件夹。")

if __name__ == "__main__":
    main()