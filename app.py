import streamlit as st
import requests

# 시크릿에서 OC 값 불러오기
oc = st.secrets["OC"]

# Streamlit 페이지 기본 설정
st.set_page_config(page_title="법령 검색 테스트", page_icon="📘")
st.title("📘 법령정보 검색 테스트")
st.info("법령명을 입력하면 국가법령정보센터 DRF API로 결과를 가져옵니다.")

# 사용자 입력 받기
keyword = st.text_input("🔍 검색할 법령명을 입력하세요 (예: 형법, 민법):")

if keyword:
    with st.spinner("🔍 검색 중..."):
        url = f"https://www.law.go.kr/DRF/lawSearch.do?OC={oc}&target=law&type=JSON&query={keyword}"
        response = requests.get(url)

        if response.status_code == 200:
            try:
                data = response.json()
                if "law" in data and data["law"]:
                    for law in data["law"]:
                        st.markdown(f"### 📘 {law['법령명한글']}")
                        st.write(f"📄 법령ID: {law['법령ID']}")
                        st.divider()
                else:
                    st.warning("🔍 검색 결과가 없습니다.")
            except Exception as e:
                st.error(f"❌ JSON 파싱 오류: {e}")
        else:
            st.error(f"❌ API 호출 실패 (상태코드: {response.status_code})")
