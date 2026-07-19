import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(
    page_title="MEC College Chatbot",
    page_icon="🎓",
    layout="centered"
)

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
client = Groq()

SYSTEM_PROMPT = """
You are an AI assistant for Muthayammal Engineering College.

You help students by answering questions about:
- Departments
- Courses
- Admissions
- Placements
- Hostel
- Library
- Campus
- Events
- Timetable
- Faculty
- General college information

If you don't know the exact answer, politely ask the student to contact the college office.

Be polite, friendly, and keep answers short.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🎓 Muthayammal Engineering College Chatbot")
st.caption("Ask anything about the college")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask about departments, placements, hostel, fees..."):

    with st.chat_message("user"):
        st.write(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    api_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    api_messages.extend(st.session_state.messages)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=api_messages,
                temperature=0.5,
                max_tokens=500
            )

            reply = response.choices[0].message.content
            st.write(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

with st.sidebar:
    st.header("🎓 About")

    st.write("""
**Muthayammal Engineering College AI Assistant**

You can ask about:

✅ Departments

✅ Courses

✅ Placements

✅ Hostel

✅ Library

✅ Campus Facilities

✅ Events

✅ Timetable

✅ Admissions
""")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption(f"Messages: {len(st.session_state.messages)}")



