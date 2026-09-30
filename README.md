# 唐山美食旅游助手 🍜

一个面向唐山本地旅游场景的**大模型智能问答应用**，使用 **RAG（检索增强生成）** 技术，为用户提供景点、美食、行程、交通等本地问答服务。

## ✨ 功能

- 基于唐山旅游知识库（景点/美食/行程/交通）的智能问答
- RAG 检索增强：先检索相关资料，再让大模型基于资料回答，减少幻觉
- 两种运行方式：命令行版（chat.py）与网页版（Streamlit，app.py）
- 多轮对话支持

## 🛠 技术栈

- **Python 3**
- **DeepSeek 大模型 API**（OpenAI SDK 调用）
- **RAG 检索增强生成**（文档切块 + 关键词检索 + Prompt 拼装）
- **Streamlit**（网页界面）
- **Coze**（另有一版零代码 Agent 实现）

## 🚀 快速开始

### 1. 获取 API Key

到 [DeepSeek 开放平台](https://platform.deepseek.com) 注册并创建 API Key。

### 2. 安装依赖

```bash
pip install openai streamlit
```

### 3. 设置环境变量

```bash
# Windows CMD
set DEEPSEEK_API_KEY=sk-你的key

# Windows PowerShell
$env:DEEPSEEK_API_KEY="sk-你的key"
```

### 4. 运行

命令行版：

```bash
python chat.py
```

网页版：

```bash
streamlit run app.py
```

浏览器会自动打开对话页面。

## 📂 项目结构

```
tangshan_agent/
├── app.py               # Streamlit 网页版（含 RAG）
├── chat.py              # 命令行版
└── 唐山旅游攻略.txt      # 知识库资料
```

## 📌 说明

- 本项目为个人学习项目，用于大模型应用方向求职作品展示。
- API Key 请通过环境变量配置，请勿硬编码或提交到仓库。
