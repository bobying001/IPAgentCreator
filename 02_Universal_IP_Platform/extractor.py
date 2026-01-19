import os
import pdfplumber
import docx
import chardet
from tqdm import tqdm

def extract_pdf(path):
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
    return text

def extract_docx(path):
    try:
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_txt(path):
    try:
        with open(path, 'rb') as f:
            raw = f.read()
            encoding = chardet.detect(raw)['encoding'] or 'utf-8'
        return raw.decode(encoding, errors='ignore')
    except Exception as e:
        return f"Error reading TXT: {str(e)}"

def run_extractor():
    base_dir = os.path.dirname(__file__)
    docs_dir = os.path.join(base_dir, "source_documents")
    target_dir = os.path.join(base_dir, "raw_text")
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    files = [f for f in os.listdir(docs_dir) if f.endswith(('.pdf', '.docx', '.txt'))]
    if not files:
        print(f"💡 没有在 {docs_dir} 找到可处理的文件。")
        return

    print(f"📦 启动格式转换器，共计 {len(files)} 个文件...")
    for filename in tqdm(files, desc="提取文字"):
        path = os.path.join(docs_dir, filename)
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == '.pdf':
            content = extract_pdf(path)
        elif ext == '.docx':
            content = extract_docx(path)
        elif ext == '.txt':
            content = extract_txt(path)
        else:
            continue
            
        target_name = filename + ".txt"
        with open(os.path.join(target_dir, target_name), 'w', encoding='utf-8') as f:
            f.write(content)
    print(f"✅ 转换完成，文字已存入: {target_dir}")

if __name__ == "__main__":
    run_extractor()
