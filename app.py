import requests
import streamlit as st
import xml.etree.ElementTree as ET  # XML 파싱용

# ✅ Streamlit Secrets에 저장한 API 키 불러오기
law_api_key = st.secrets["LAW_API_KEY"]

# ✅ 사용자 검색어 입력 받기
law_keyword = st.text_input("🔍 검색할 법령명을 입력하세요 (예: 형법, 민법):")

if law_keyword:
    # ✅ API 호출
    url = "http://apis.data.go.kr/1170000/law/lawSearchList.do"
    params = {
        "serviceKey": law_api_key,
        "target": "law",
        "query": law_keyword,
        "numOfRows": "10",
        "pageNo": "1",
        "type": "xml"
    }
    response = requests.get(url, params=params)

    # ✅ 결과 파싱 및 출력
    if response.status_code == 200:
        st.success("📜 법령 검색 결과:")
        try:
            root = ET.fromstring(response.content)
            items = root.findall(".//law")  # XML 구조에 따라 수정 가능
            if not items:
                st.warning("검색 결과가 없습니다.")
            for item in items:
                name = item.find("법령명한글").text if item.find("법령명한글") is not None else "제목 없음"
                revision = item.find("제개정구분명").text if item.find("제개정구분명") is not None else "내용 없음"
                st.markdown(f"### 📘 {name}\n- 제개정 구분: {revision}\n---")
        except Exception as e:
            st.error(f"❌ XML 파싱 중 오류 발생: {e}")
    else:
        st.error(f"❌ API 호출 실패 (상태코드: {response.status_code})")



