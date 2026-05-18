import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# 1. 데이터 로딩 함수 정의 (캐싱 처리)
@st.cache_data
def load_background_data():
    # --- 1번 데이터: 자동차등록대수현황 (Excel) ---
    path1 = "raw_data/KOSIS_자동차등록대수현황.xlsx"
    df_kosis = pd.read_excel(path1)

    # --- 2번 데이터: 전기차등록현황 (Excel / .xls 형식이므로 engine='xlrd' 필요할 수 있음) ---
    path2 = "raw_data/201001_202605_전기차등록현황.xls"
    # 구형 .xls 파일인 경우 xlrd 라이브러리가 필요합니다.
    df_ev_reg = pd.read_excel(path2)

    # --- 3번 데이터: MySQL DB (ev_station_seoul 테이블) ---
    # DB 연결 정보 (사용자 정보에 맞춰 수정하세요)
    # 예: mysql+pymysql://user:password@host:port/mydb
    engine = create_engine('mysql+pymysql://root:password@localhost:3306/mydb')
    query = "SELECT * FROM ev_station_seoul"
    df_ev_station = pd.read_sql(query, engine)

    return df_kosis, df_ev_reg, df_ev_station

# 2. 메인 앱 로직
def main():
    st.title("자동차 및 전기차 현황 대시보드")
    
    with st.spinner('데이터를 백그라운드에서 불러오는 중...'):
        # 함수를 실행하면 최초 1회만 로딩하고 이후엔 캐시된 데이터를 사용합니다.
        kosis_data, ev_reg_data, ev_station_data = load_background_data()

    # 3. 데이터 활용 예시
    st.subheader("📊 데이터 확인")
    
    tab1, tab2, tab3 = st.tabs(["KOSIS 자동차 현황", "전기차 등록 현황", "서울 충전소 DB"])
    
    with tab1:
        st.write("KOSIS 엑셀 데이터")
        st.dataframe(kosis_data.head())

    with tab2:
        st.write("2010~2026 전기차 등록 데이터")
        st.dataframe(ev_reg_data.head())

    with tab3:
        st.write("MySQL DB: 서울 충전소 데이터")
        st.dataframe(ev_station_data.head())

if __name__ == "__main__":
    main()