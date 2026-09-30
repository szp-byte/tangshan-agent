# -*- coding: utf-8 -*-
"""
唐山美食旅游助手 - 阶段4 命令行版
用 Python 调用大模型 API，实现"输入问题 -> AI回答"

使用前：
1. 去平台注册拿到 API Key（豆包用火山方舟，或 DeepSeek 官方平台）
2. 把下面的 API_KEY 换成你的 Key
3. 运行：python chat.py
"""
import os
from openai import OpenAI

# ===== API Key：从环境变量读取（不要硬编码在代码里） =====
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-你的API-KEY")                          # 改成你的
BASE_URL = "https://api.deepseek.com"               # DeepSeek 用这个
MODEL = "deepseek-chat"                             # DeepSeek 用 deepseek-chat
# 如果用豆包(火山方舟)，改成：
# BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
# MODEL = "你的接入点ID"
# ============================

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 人设（和你扣子里的一样）
SYSTEM_PROMPT = """你是唐山本地美食旅游助手，负责回答关于唐山景点、美食、行程的问题。

回复要求：
1. 介绍景点或美食时，尽量给出地址、价格、营业时间；
2. 语言口语化、简洁，单次回答不超过200字；
3. 资料里查不到的信息，如实说明"暂时不了解"，不要编造。
当用户问"怎么安排几天行程"时，给出可执行的日程安排。
"""

print("=" * 40)
print("唐山美食旅游助手（Python版）")
print("输入问题，回车发送；输入 quit 退出")
print("=" * 40)

while True:
    user_input = input("\n你问：")
    if user_input.strip().lower() == "quit":
        print("再见！")
        break

    # 调用大模型
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        stream=False,
    )

    answer = resp.choices[0].message.content
    print("\nAI答：", answer)
