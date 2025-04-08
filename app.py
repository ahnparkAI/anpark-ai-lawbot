import streamlit as st
import openai
import requests
import xml.etree.ElementTree as ET

# ✅ API 키 불러오기
openai.api_key = st.secrets["OPENAI_API_KEY"]
law_api_key = st.secrets["LAW_API_KEY"]

# ✅ 사용자 질문 입력
user_question = st.text_input("💬 궁금한 법률 질문을 입력하세요:")

if user_question:
    with st.spinner("법령 검색 중..."):
        # 1. GPT에 키워드 추출 요청
        keyword_prompt = f"다음 질문에서 법령 검색에 적합한 핵심 키워드를 한 단어 또는 짧은 문장으로 알려줘.\n\n질문: {user_question}"
        keyword_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 한국 법률 키워드 분석가야."},
                {"role": "user", "content": keyword_prompt}
            ]
        )
        keyword = keyword_response['choices'][0]['message']['content'].strip()
        st.info(f"🔎 추출된 키워드: `{keyword}`")

        # 2. 법령정보센터 API 호출
        law_url = "http://apis.data.go.kr/1170000/law/lawSearchList.do"
        law_params = {
            "serviceKey": law_api_key,
            "target": "law",
            "query": keyword,
            "numOfRows": "3",
            "pageNo": "1",
            "type": "xml"
        }
        response = requests.get(law_url, params=law_params)

        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                items = root.findall(".//law")
                if not items:
                    st.warning("관련 법령을 찾지 못했어요.")
                else:
                    # 3. 첫 번째 법령 텍스트 추출
                    law_name = items[0].find("법령명한글").text if items[0].find("법령명한글") is not None else "알 수 없음"
                    law_status = items[0].find("제개정구분명").text if items[0].find("제개정구분명") is not None else "정보 없음"

                    # 4. GPT에 법령 기반 해석 요청
                    law_prompt = f"아래는 법령명과 제개정 정보입니다. 사용자 질문에 대해 한국 법률 전문가처럼 답변해주세요.\n\n" \
                                 f"[법령명] {law_name}\n[제개정] {law_status}\n\n[질문] {user_question}"

                    answer_response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "너는 한국 법률 전문가야. 법령 정보를 바탕으로 친절하게 설명해줘."},
                            {"role": "user", "content": law_prompt}
                        ]
                    )
                    answer = answer_response['choices'][0]['message']['content']
                    st.success("✅ GPT 법률 해석 결과:")
                    st.write(answer)
            except Exception as e:
                st.error(f"❌ XML 파싱 오류: {e}")
        else:
            st.error(f"❌ 법령 API 호출 실패 (상태코드: {response.status_code})")
