import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)


from dotenv import load_dotenv
# 環境変数の読み込み
load_dotenv()

#プロンプトテンプレートの作成
template = """
あなたは聞かれた質問に答える優秀なアシスタントです。
以下に株式会社Nucoの会社情報を書きます。

会社概要

会社名
株式会社Nuco
(English : Nuco Inc.)

設立日
2017年6月12日

代表者名
小山内美悠

所在地
〒150-0011
東京都渋谷区東1-26-20
東京建物東渋谷ビル 6F

事業内容
AIシステムの企画・開発・運営・販売

お問い合わせ
https://nuco.co.jp/contact

サービス例
データ活用コンサルティング
大規模データ基盤構築
AIシステム開発
AI人材育成コンサルティング
機械学習セミナー

これを元に質問に答えてください。
"""

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}"),
])

@st.cache_resource
def load_conversation():
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0
    )
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(
        memory=memory,
        prompt=prompt,
        llm=llm)
    return conversation


# Streamlitによって、タイトル部分のUIをの作成
st.title("Nuco Chatbot")
st.caption("Nuco Inc.")
st.write("株式会社Nucoについての質問に答えます。")

if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []

user_message = st.text_area("質問を入力してください")
submitted = st.button("送信")

if submitted:
    conversation = load_conversation()
    answer = conversation.predict(input=user_message)

    st.session_state.generated.append(answer)
    st.session_state.past.append(user_message)

    # 質問送信後にsubmittedの値をリセットする
    submitted = False

if st.session_state["generated"]:
    for i in range(len(st.session_state.generated) - 1, -1, -1):
        message(st.session_state.generated[i], key=str(i))
        message(st.session_state.past[i], is_user=True, key=str(i) + "_user")
