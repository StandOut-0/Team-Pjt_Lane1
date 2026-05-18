import streamlit as st
import json


def load_faq():
    try:
        with open("faq_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def find_answer(question, faq_data):

    lower_question = question.lower()

    best_match = None
    highest_score = 0

    for faq in faq_data:

        score = 0

        title = faq["title"].lower()
        answer = faq["answer"].lower()

        keywords = lower_question.split()

        for keyword in keywords:

            if keyword in title:
                score += 2

            if keyword in answer:
                score += 1

        if lower_question in title:
            score += 5

        if score > highest_score:
            highest_score = score
            best_match = faq

    if best_match:
        return best_match["answer"]

    return "죄송합니다. 답변을 찾지 못했습니다."


def render_chat_interface():

    # st.markdown("## 💬 EV 챗봇")

    faq_data = load_faq()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "안녕하세요! 무엇을 도와드릴까요?"
            }
        ]

    # 기존 메시지 출력
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 입력창
    user_input = st.chat_input("질문 입력...")

    if user_input:

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        # 챗봇 응답 생성
        response = find_answer(user_input, faq_data)

        # 챗봇 메시지 저장
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        with st.chat_message("assistant"):
            st.markdown(response)