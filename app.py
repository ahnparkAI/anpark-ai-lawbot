import streamlit as st
import openai

st.set_page_config(page_title="안팍 법률 비서", page_icon="⚖️")

st.title("⚖️ 안팍 법률 비서 챗봇")
st.markdown("GPT를 활용한 똑똑한 법률 조언 챗봇입니다. 궁금한 법률 상황을 입력해보세요.")

user_question = st.text_input("💬 법률 질문을 입력하세요:")

if user_question:
    with st.spinner("답변 생성 중..."):
        try:
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "너는 한국 법률 전문가야. 질문을 분석해서 관련된 법 조항이나 범죄 유형을 제시해줘."},
                    {"role": "user", "content": user_question}
                ]
            )

            answer = response.choices[0].message.content
            st.markdown("### 📘 답변")
            st.write(answer)
        except Exception as e:
            st.error(f"오류 발생: {e}")
else:
    st.info("왼쪽 상단 톱니바퀴 → Secrets에 OpenAI API 키를 먼저 설정해 주세요.")
