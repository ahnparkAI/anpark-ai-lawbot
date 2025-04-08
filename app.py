import requests
import streamlit as st
import xml.etree.ElementTree as ET  # XML 파싱용

# ✅ API 키
law_api_key = st.secrets["LAW_API_KEY"]

# ✅ 사용자 검색어 입력 받기
law_keyword = st.text_input("🔍 검색할 법령명을 입력하세요 (예: 형법, 민법):")

if law_keyword:
    # ✅ API 호출
    url = "http://apis.data.go.kr/1170000/law"
    params = {
        "serviceKey": law_api_key,
        "search": law_keyword,
        "type": "xml"
    }
    response = requests.get(url, params=params)

    # ✅ 결과 파싱 및 출력
    if response.status_code == 200:
        st.success("📜 법령 검색 결과:")
        try:
            root = ET.fromstring(response.text)
            for item in root.iter("item"):  # item 항목 반복
                name = item.find("lawName").text if item.find("lawName") is not None else "제목 없음"
                summary = item.find("contents").text if item.find("contents") is not None else "내용 없음"
                st.markdown(f"### 📘 {name}\n{summary}\n---")
        except Exception as e:
            st.error(f"❌ XML 파싱 중 오류 발생: {e}")
    else:
        st.error(f"❌ API 호출 실패 (상태코드: {response.status_code})")

