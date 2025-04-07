import openai
import streamlit as st

# OpenAI API Key 가져오기
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="안팍 법률 비서", page_icon="⚖️")
st.title("⚖️ 안팍 법률 비서 챗봇")
st.info("💬 GPT를 활용한 똑똑한 법률 조언 챗봇입니다. 궁금한 법률 상황을 입력해보세요.")

user_question = st.text_input("📄 법률 질문을 입력하세요:")

if user_question:
    with st.spinner("답변 생성 중..."):
        try:
            # 최신 API 방식으로 응답 받기
            response = openai.Completion.create(
                model="gpt-3.5-turbo",  # 최신 모델 사용
                prompt=user_question,  # 사용자 질문을 프롬프트로 사용
                max_tokens=100
            )
            answer = response['choices'][0]['text']
            st.success("✅ 답변")
            st.write(answer)
        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")
