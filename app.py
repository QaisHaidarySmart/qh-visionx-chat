import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="QH VisionX AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("QH VisionX Chatbot")
st.markdown("سامانه هوش مصنوعی پیشرفته - توسعه‌یافته توسط قیس حیدری")

api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("لطفاً کلید API را در تنظیمات هاست وارد کنید.")
else:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are QH VisionX, a professional, intelligent, and accurate AI assistant specialized in advanced technology, fluent in Dari, Persian, and English."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("پیام خود را اینجا بنویسید..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
