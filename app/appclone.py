import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

from dotenv import load_dotenv
# 環境変数の読み込み
load_dotenv()

@st.cache_resource
def load_conversation():
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0
    )
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(
        memory=memory,
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
        message(st.session_state.generated[i])
        message(st.session_state.past[i],is_user=True)
