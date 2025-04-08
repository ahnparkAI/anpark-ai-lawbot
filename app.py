import requests
import streamlit as st
import xml.etree.ElementTree as ET
import openai

# ✅ 시크릿에서 API 키 불러오기
openai_api_key = st.secrets["OPENAI_API_KEY"]
law_api_key = st.secrets["LAW_API_KEY"]

# ✅ OpenAI 클라이언트 객체 생성
client = openai.OpenAI(api_key=openai_api_key)

# ✅ 사용자 질문 입력 받기
user_question = st.text_input("📄 법률 질문을 입력하세요:")

if user_question:
    # ✅ ChatGPT에게 질문 전달
    with st.spinner("GPT에게 질문 전달 중..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "너는 한국 법률 전문가야. 질문을 분석해서 핵심 키워드를 뽑아줘."},
                    {"role": "user", "content": user_question}
                ]
            )
            keyword = response.choices[0].message.content.strip()
            st.success(f"🔑 추출된 키워드: {keyword}")
        except Exception as e:
            st.error(f"❌ GPT 오류 발생: {e}")
            keyword = ""
else:
    keyword = ""

# ✅ 키워드가 있을 때만 법령정보센터 API 호출
if keyword:
    st.divider()
    st.info("🔍 법령정보센터에서 관련 법령을 찾는 중...")

    url = "http://apis.data.go.kr/1170000/law"
    params = {
        "serviceKey": law_api_key,
        "search": keyword,
        "type": "xml"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.text)
            items = root.findall(".//item")
            if not items:
                st.warning("📭 관련된 법령이 없습니다.")
            for item in items:
                name = item.find("lawName").text if item.find("lawName") is not None else "제목 없음"
                summary = item.find("contents").text if item.find("contents") is not None else "내용 없음"
                st.markdown(f"### 📘 {name}\n{summary}\n---")
        except Exception as e:
            st.error(f"❌ XML 파싱 오류: {e}")
    else:
        st.error(f"❌ 법령정보센터 API 호출 실패 (상태코드: {response.status_code})")
