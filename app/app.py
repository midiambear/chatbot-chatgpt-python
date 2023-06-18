import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    )
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)


from dotenv import load_dotenv
# 環境変数の読み込み
load_dotenv()

import re
import requests
import argparse
import sys
from bs4 import BeautifulSoup

url = "https://nuco.co.jp/outline"
def extract_main_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    soup = BeautifulSoup(response.content, "html.parser")

    return soup



# ChatGPT-3.5のモデルのインスタンスの作成
chat = ChatOpenAI(temperature=0)

#プロンプトテンプレートの作成


# セッション内に保存されたチャット履歴のメモリの取得
try:
    memory = st.session_state["memory"]
except:
    memory = ConversationBufferMemory(return_messages=True)

# チャット用のチェーンのインスタンスの作成
chain = ConversationChain(
    llm=chat,
    memory=memory,
)

# Streamlitによって、タイトル部分のUIをの作成
st.title("Nuco Chatbot")
st.caption("Nuco Inc.")

# 入力フォームと送信ボタンのUIの作成
text_input = st.text_input("質問を入力してください")
send_button = st.button("送信")

# チャット履歴（HumanMessageやAIMessageなど）を格納する配列の初期化
history = []

# ボタンが押された時、OpenAIのAPIを実行
if send_button:
    send_button = False

    # ChatGPTの実行
    chain(text_input)

    # セッションへのチャット履歴の保存
    st.session_state["memory"] = memory

    # チャット履歴（HumanMessageやAIMessageなど）の読み込み
    try:
        history = memory.load_memory_variables({})["history"]
    except Exception as e:
        st.error(e)

# チャット履歴の表示
for index, chat_message in enumerate(reversed(history)):
    if type(chat_message) == HumanMessage:
        message(chat_message.content, is_user=True, key=2 * index)
    elif type(chat_message) == AIMessage:
        message(chat_message.content, is_user=False, key=2 * index + 1)