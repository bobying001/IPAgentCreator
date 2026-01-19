# 项目规划：通用 IP 数字化孪生工厂 (Universal IP Digital Twin Factory)

## 1. 产品愿景 (Vision)
打造一个“零代码”的智能体生产线。用户只需上传某位专家（IP）的原始著作/语料，平台即可自动完成知识萃取、逻辑重组和人格设定，最终生成可直接投喂给 Gems/GPTs 的“原子化知识库”和“系统指令”。

## 2. 核心架构 (Architecture)

### 2.1 输入层 (Input Layer)
*   **多源数据支持**：支持 PDF, DOCX, TXT, MD, 甚至音视频转录稿。
*   **IP 元数据配置**：
    *   `IP_Name`: 专家姓名 (e.g. 李中莹)
    *   `Domain`: 领域 (e.g. NLP, 投资, 健身)
    *   `Core_Values`: 核心价值观 (e.g. 三赢, 价值投资, 科学训练)

### 2.2 处理层 (The Core Engine) - "知识炼金术"
这是本产品的护城河，将之前的 `knowledge_factory.py` 泛化。

1.  **协议生成器 (Protocol Generator)**:
    *   不再手动写 `NLP_Protocol.md`，而是由 AI 根据 `Domain` 自动生成该领域的《萃取协议》。
    *   *Prompt 示例*: "你是一个知识工程专家。请为【{Domain}】领域生成一套知识原子化标准，定义什么是该领域的核心概念、实操技巧和底层逻辑。"

2.  **原子化萃取器 (Atomic Extractor)**:
    *   **Phase 1 - 概念清洗**: 识别并统一专有名词（避免同义词混淆）。
    *   **Phase 2 - 逻辑压缩**: 将长篇案例转化为 `[Context] -> [Action] -> [Result]` 结构。
    *   **Phase 3 - 话术克隆**: 提取 IP 的口头禅和典型句式。

3.  **索引构建器 (Index Builder)**:
    *   自动生成知识图谱式的 `MASTER_INDEX.md`，不再仅仅是列表，而是从“新手入门”到“高阶精通”的学习路径。

### 2.3 输出层 (Output Layer)
*   **Deliverable A: 知识库包 (.zip)**
    *   包含所有 `_Atomic.md` 文件。
*   **Deliverable B: 角色说明书 (Instructions)**
    *   自动生成的 Prompt，包含：角色设定、决策树、知识库调用规则、禁忌事项。

## 3. MVP 实施路线图 (Roadmap)

### Phase 1: 命令行工具 (CLI Ver.) - *当前阶段*
*   **目标**: 验证“协议生成器”的泛化能力。
*   **Action**:
    *   改造 `knowledge_factory.py`，将其中硬编码的“李中莹”和“NLP”替换为变量。
    *   尝试跑通另一个完全不同的 IP（如：巴菲特-投资，或 只有少量文档的公司内部 SOP）。

### Phase 2: 简易 Web UI (Streamlit/Next.js)
*   **目标**: 让非技术人员也能上传文件。
*   **功能**:
    *   文件上传区 (Drag & Drop)。
    *   进度条显示（解析中... 萃取中...）。
    *   结果下载区。

### Phase 3: 智能体对接口 (API Integration)
*   **目标**: 这是一个高级功能，直接通过 API 将生成的 Instructions 推送到支持 API 创建 Agent 的平台（如 Dify, FastGPT 等，目前 Google Gems 暂不支持 API 创建，需手动）。

## 4. 关键技术难点预判
*   **噪声处理**: 如何处理扫描件中的乱码（需集成 OCR）。
*   **矛盾消解**: 当 IP 在不同时期的书里说了矛盾的话（如早期说 A，晚期说 Not A），系统需要具备“版本管理”或“晚期优先”的逻辑。
*   **风格迁移**: 确保生成的 Instructions 能精准捕捉 IP 的“味儿”。

## 5. 商业价值
*   **To B**: 帮助企业快速利用内部文档生成“金牌销售陪练”、“新员工导师”。
*   **To C**: 帮助创作者将自己的公众号/专栏文章瞬间变成“数字分身”。
