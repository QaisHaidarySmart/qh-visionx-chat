import os
import streamlit as st
from groq import Groq
import dotenv

# بارگذاری API Key
dotenv.load_dotenv() if os.path.exists(".env") else None
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("QH VisionX Chatbot")
st.markdown("**سامانه هوش مصنوعی پیشرفته** — ساخته‌شده با عشق و خلاقیت توسط قیس حیدری")
st.caption("🐉 نسخه شاعرانه | Powered by Groq Qwen3.6 27B | Jadu + Shaeri")

# ذخیره پیام‌های قبلی
if "messages" not in st.session_state:
    st.session_state.messages = []

# نمایش پیام‌های قبلی (با سبک شاعرانه)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==================== دکمه پاک‌سازی تاریخچه ====================
if st.button("🗑️ پاک‌سازی تاریخچه جادویی", type="secondary", help="مکالمه را مثل غباری بر باد بده"):
    st.session_state.messages = []
    st.rerun()
# ==============================================================

# ورودی کاربر
if prompt := st.chat_input("سوال شاعرانه‌ات را بپرس..."):
    # اضافه کردن پیام کاربر
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"**شاعر:** {prompt}")

    # درخواست به Groq (ساختار کامل + خلاصه‌سازی خودکار)
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="qwen/qwen3.6-27b",                     # قوی‌ترین مدل فارسی (بر اساس بررسی‌های ۲۰۲۶)
            messages=st.session_state.messages,
            stream=True,
            temperature=0.8,                               # خلاقیت بیشتر
            max_tokens=2048,
        )
        
        response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

    # ==================== خلاصه‌سازی هوشمند خودکار ====================
    # هر ۶ پیام کاربر = خلاصه جادویی (خودکار)
    if len(st.session_state.messages) > 10:
        summary_prompt = (
            "شما یک شاعر خلاق ایرانی هستید. فقط یک خلاصه کوتاه، زیبا و جادویی (حداکثر ۴۰ توکن) از تمام مکالمه بنویسید. "
            "موضوع اصلی، حس‌ها، حکمت و نکات کلیدی را به صورت شعرگونه و شاعرانه بیان کنید. "
            "فقط به فارسی بنویسید، هیچ توضیحی ندهید."
        )
        
        summary_messages = [
            {"role": "system", "content": "شما یک شاعر جادویی هستید که کلمات را مثل شمشیر به قلب مخاطب می‌زند."},
            {"role": "user", "content": summary_prompt},
            {"role": "user", "content": "مکالمه کامل:\n" + "\n".join(
                f"{m['role']}: {m['content']}" for m in st.session_state.messages
            )}
        ]
        
        with st.chat_message("system"):  # خلاصه را به عنوان پیام سیستم نشان می‌دهیم
            summary_response = ""
            stream_summary = client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=summary_messages,
                stream=True,
                temperature=0.6,
                max_tokens=128,
            )
            for chunk in stream_summary:
                if chunk.choices[0].delta.content:
                    summary_response += chunk.choices[0].delta.content
                    st.markdown(summary_response)
            
            # ذخیره خلاصه
            summary_message = {"role": "system", "content": summary_response}
            st.session_state.messages = [summary_message]
    # ===========================================================================
