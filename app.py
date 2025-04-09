import streamlit as st
import openai
import requests
from urllib.parse import quote

# ✅ 시크릿에서 API 키 불러오기
openai.api_key = st.secrets["OPENAI_API_KEY"]
oc = st.secrets["OC"]

# ✅ Streamlit 설정
st.set_page_config(page_title="프로젝트 안팍", page_icon="⚖️")
st.title("⚖️ 안팍 법률 비서")
st.info("프로젝트 안팍")

# ✅ 사용자 질문 입력
user_question = st.text_input("📌 법률 질문을 입력하세요:")

if user_question:
    with st.spinner("관련 법령 검색 중..."):
        # 1. GPT에게 키워드 추출 요청
        try:
            gpt_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "다음 질문에서 관련 법령 키워드를 1~2개만 추출해줘. 예: 형법, 민법 등"},
                    {"role": "user", "content": user_question}
                ]
            )
            keyword = gpt_response.choices[0].message.content.strip().split("\n")[0]
            encoded_keyword = quote(keyword)

            # 2. 법제처 DRF API로 법령 검색
            law_url = f"https://www.law.go.kr/DRF/lawSearch.do?OC={oc}&target=law&type=JSON&query={encoded_keyword}"
            law_res = requests.get(law_url)

            if law_res.status_code == 200 and 'law' in law_res.json():
                law_list = law_res.json()['law']
                if law_list:
                    law_id = law_list[0]['법령ID']
                    law_name = law_list[0]['법령명한글']

                    # 3. 법령 상세 가져오기
                    detail_url = f"https://www.law.go.kr/DRF/lawService.do?OC={oc}&target=law&type=JSON&lawId={law_id}"
                    detail_res = requests.get(detail_url)

                    if detail_res.status_code == 200:
                        law_text = detail_res.json()['law']['조문'][0]['조문내용'][:1500]  # 일부만 사용

                        # 4. GPT에게 설명 요청
                        answer_res = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "너는 한국 법률 전문가야. 사용자가 궁금한 내용을 이해하고 관련 법령 내용을 바탕으로 설명해줘."},
                                {"role": "user", "content": f"질문: {user_question}\n관련 법령 내용: {law_text}"}
                            ]
                        )

                        st.success(f"📘 {law_name} 관련 답변")
                        st.write(answer_res.choices[0].message.content)
                    else:
                        st.error("법령 전문 조회에 실패했습니다.")
                else:
                    st.warning("관련 법령을 찾을 수 없습니다.")
            else:
                st.error("법령 검색 실패 또는 OC 코드 오류")
        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")
