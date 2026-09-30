# -*- coding: utf-8 -*-
"""
唐山美食旅游助手 - 阶段4升级版（RAG检索增强生成 + Streamlit网页）

核心思路（面试要能讲）：
1. 读取《唐山旅游攻略》文档并切块；
2. 用户提问 -> 从知识库检索最相关的资料块（关键词打分）；
3. 把检索到的资料拼进 Prompt -> 交给大模型回答（RAG：检索增强生成）。

运行：streamlit run app.py
"""
import os
import re
import streamlit as st
from openai import OpenAI

# ===== API Key：从环境变量读取（不要硬编码在代码里） =====
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-你的API-KEY")
BASE_URL = "https://api.deepseek.com"               # DeepSeek 用这个
MODEL = "deepseek-chat"                             # DeepSeek 用 deepseek-chat
# ============================

# 知识库文档路径（放在项目同目录）
KNOWLEDGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "唐山旅游攻略.txt")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ---------- 1. 读取并切块 ----------
def load_chunks(path, chunk_size=120, overlap=25):
    """把攻略文档切成有重叠的片段块"""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    body = "\n".join(lines)
    chunks = []
    start = 0
    while start < len(body):
        chunks.append(body[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks

CHUNKS = load_chunks(KNOWLEDGE_FILE)

# ---------- 2. 关键词检索相关块 ----------
STOP = set("的是在有了和与就都而及于是然后你要怎么吗啥哪些有")

def tokenize(text):
    """简单的中文切词：去掉停用词，返回词列表"""
    text = re.sub(r"[\s\W_]+", "", text)  # 去空格和标点
    words = []
    for ch in text:
        if ch not in STOP and not ch.isdigit() and ch.isalpha():
            words.append(ch)
    # 也加入双字组合，提升匹配度
    bigrams = ["".join(text[i:i+2]) for i in range(len(text)-1) if all(c not in STOP for c in text[i:i+2])]
    return set(words) | set(bigrams)

def search(query, top_k=3):
    """检索与问题最相关的top_k个片段（基于关键词重合度打分）"""
    q_words = tokenize(query)
    scored = []
    for i, c in enumerate(CHUNKS):
        c_words = tokenize(c)
        # 重合度 = 问题关键词在片段里命中的数量
        hit = len(q_words & c_words)
        if hit > 0:
            scored.append((hit, i, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]

# ---------- 3. 组装回答 ----------
SYSTEM_PROMPT = """你是唐山本地美食旅游助手，负责回答关于唐山景点、美食、行程的问题。

回复要求：
1. 优先依据【参考资料】回答，参考资料里查不到的信息，如实说明"暂时不了解"，不要编造；
2. 介绍景点或美食时，尽量给出地址、价格、营业时间；
3. 语言口语化、简洁，单次回答不超过200字；
4. 当用户问"怎么安排几天行程"时，给出可执行的日程安排。

【参考资料】
{context}"""

def ask(question):
    # 检索相关资料
    hits = search(question)
    context = "\n\n".join(f"[资料{i+1}] {c}" for _, i, c in hits)
    if not context:
        context = "（未检索到相关资料，请如实说明）"

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
            {"role": "user", "content": question},
        ],
        stream=False,
    )
    return resp.choices[0].message.content, hits

# ---------- 网页界面 ----------
st.set_page_config(page_title="唐山美食旅游助手", page_icon="🍜")
st.title("🍜 唐山美食旅游助手")
st.caption("AI 智能问答 · 基于大模型API + RAG知识检索")
st.success(f"已加载知识库：{len(CHUNKS)} 个资料片段，可回答攻略中的景点、美食、行程、交通问题")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if q := st.chat_input("问点唐山的事：清东陵怎么去？唐山有什么好吃的？"):
    with st.chat_message("user"):
        st.write(q)
    st.session_state.messages.append({"role": "user", "content": q})

    with st.chat_message("assistant"):
        with st.spinner("正在检索知识库并思考..."):
            answer, hits = ask(q)
            st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # 调试信息：显示检索到哪几条资料（讲解时可展示）
    with st.expander("🔍 查看本次检索到的知识库片段"):
        if hits:
            for score, i, c in hits:
                st.write(f"匹配 {score} 个关键词 | {c[:80]}...")
        else:
            st.write("未检索到相关片段")
