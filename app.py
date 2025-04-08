import streamlit as st
import requests
import xml.etree.ElementTree as ET

# 시크릿에서 API 키 불러오기
law_api_key = st.secrets["LAW_API_KEY"]

# 페이지 설정
st.set_page_config(page_title="법령 검색기", page_icon="📚")
st.title("📚 법령정보센터 API 검색기")
st.info("법령명을 입력하면 국가법령정보센터에서 관련 정보를 조회합니다.")

# 사용자 입력 받기
law_keyword = st.text_input("🔍 검색할 법령명을 입력하세요 (예: 형법, 민법):")

if law_keyword:
    with st.spinner("🔎 법령 검색 중..."):
        url = "http://apis.data.go.kr/1170000/law"
        params = {
            "serviceKey": law_api_key,
            "search": law_keyword,
            "type": "xml"
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                items = root.findall(".//item")
                if not items:
                    st.warning("❗ 관련 법령을 찾을 수 없습니다.")
                for item in items:
                    name = item.findtext("lawName", default="제목 없음")
                    summary = item.findtext("contents", default="내용 없음")
                    st.markdown(f"### 📘 {name}\n{summary}\n---")
            except Exception as e:
                st.error(f"❌ XML 파싱 오류: {e}")
        else:
            st.error(f"❌ API 호출 실패 (상태코드: {response.status_code})")
