import streamlit as st
import openai
import requests

# ✅ 시크릿에서 키 불러오기
openai.api_key = st.secrets["OPENAI_API_KEY"]
oc = st.secrets["OC"]

st.set_page_config(page_title="안팍 법률 비서", page_icon="⚖️")
st.title("⚖️ 안팍 법률 비서 챗봇")
st.info("GPT와 국가법령정보센터 DRF API를 활용한 법률 비서입니다. 궁금한 법령명을 입력하세요.")

# ✅ 사용자 입력
keyword = st.text_input("📘 검색할 법령명을 입력하세요:")

if keyword:
    with st.spinner("법령 검색 중..."):
        # 1. 검색어로 법령 목록 조회
        list_url = f"https://www.law.go.kr/DRF/lawSearch.do?OC={oc}&target=law&type=JSON&query={keyword}"
        list_res = requests.get(list_url)

        if list_res.status_code == 200:
            try:
                law_list = list_res.json()
                if 'law' not in law_list or not law_list['law']:
                    st.warning("검색 결과가 없습니다.")
                else:
                    # 첫 번째 법령 선택
                    law_id = law_list['law'][0]['법령ID']
                    law_name = law_list['law'][0]['법령명한글']

                    # 2. 법령 ID로 전문 조회
                    detail_url = f"https://www.law.go.kr/DRF/lawService.do?OC={oc}&target=law&type=JSON&lawId={law_id}"
                    detail_res = requests.get(detail_url)
                    if detail_res.status_code == 200:
                        law_data = detail_res.json()
                        raw_text = law_data['law']['조문'][0]['조문내용'][:1500]  # 일부만 추출

                        # 3. GPT에게 요약 요청
                        st.success(f"📑 {law_name} 요약 결과")
                        try:
                            response = openai.ChatCompletion.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {"role": "system", "content": "너는 법률 전문가야. 사용자가 입력한 법령의 내용을 간단히 요약해줘."},
                                    {"role": "user", "content": raw_text}
                                ]
                            )
                            answer = response.choices[0].message.content
                            st.markdown(answer)
                        except Exception as e:
                            st.error(f"GPT 오류 발생: {e}")
                    else:
                        st.error("법령 상세 정보를 가져오는 데 실패했습니다.")
            except Exception as e:
                st.error(f"JSON 파싱 오류: {e}")
        else:
            st.error(f"법령 검색 실패 (상태코드 {list_res.status_code})")
