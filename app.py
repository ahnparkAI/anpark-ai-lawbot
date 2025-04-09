import streamlit as st
import openai
import requests
import json

# ✅ 시크릿에서 키 불러오기
openai_api_key = st.secrets["OPENAI_API_KEY"]
oc = st.secrets["OC"]

# ✅ OpenAI 설정
client = openai.OpenAI(api_key=openai_api_key)

# ✅ 입력 받기
question = st.text_input("📘 법률 질문을 입력하세요:")

if question:
    with st.spinner("GPT가 관련 법령 키워드 분석 중..."):
        try:
            gpt_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "너는 한국 법률 전문가야. 사용자 질문에서 법령 키워드를 1~2개로 요약해줘."},
                    {"role": "user", "content": question}
                ]
            )
            keyword = gpt_response.choices[0].message.content.strip()
            st.success(f"📌 추출 키워드: {keyword}")

            # ✅ 법령정보센터 API 호출
            url = f"https://www.law.go.kr/DRF/lawSearch.do?OC={oc}&target=law&type=JSON&query={keyword}"
            law_response = requests.get(url)

            if law_response.status_code == 200:
                law_data = law_response.json()
                if law_data["Law"] and "lawName" in law_data["Law"][0]:
                    result_text = f"🔍 관련 법령: **{law_data['Law'][0]['lawName']}**\n\n📄 법령요약: {law_data['Law'][0]['lawSummary']}"
                    st.markdown(result_text)
                else:
                    st.warning("❗ 관련 법령을 찾을 수 없습니다.")
            else:
                st.error(f"법령정보센터 API 호출 실패 - 상태 코드: {law_response.status_code}")

        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")

