import os
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from db import get_engine


get_engine()
# .env 파일 로드
load_dotenv()

# ----------------- [ 데이터 로드 영역 ] -----------------
@st.cache_data # 데이터 속도 향상을 위한 캐싱
def load_dashboard_data():
    engine = get_engine()
    
    # 📌 [요구사항 1 반영] 2020-10 ~ 2025-10 데이터만 필터링하여 가져오기
    # (앞선 적재 단계에서 날짜를 YYYY-MM 형태로 통일했으므로 하이픈 기준으로 조회합니다)
    query_ev = """
        SELECT `date`, `seoul` AS `ev_cnt`
        FROM ev_car
        WHERE `date` BETWEEN '2020-10' AND '2025-10'
        ORDER BY `date` ASC;
    """
    
    query_ratio = """
        SELECT `date`, `seoul` AS `total_cnt`
        FROM ev_car_ratio
        WHERE `date` BETWEEN '2020-10' AND '2025-10'
        ORDER BY `date` ASC;
    """
    
    df_ev = pd.read_sql(query_ev, con=engine)
    df_ratio = pd.read_sql(query_ratio, con=engine)
    
    # 두 테이블 정보를 날짜(date) 기준으로 결합(Join)
    df_merged = pd.merge(df_ev, df_ratio, on='date', how='inner')
    
    # 📌 [요구사항 2 반영] 내연기관 차 값 계산: (전체 차량 수) - (전기차 수)
    df_merged['ice_cnt'] = df_merged['total_cnt'] - df_merged['ev_cnt']
    
    return df_merged

# 데이터 가져오기
try:
    df = load_dashboard_data()
except Exception as e:
    st.error(f"데이터베이스 연결 및 로드 실패: {e}")
    st.stop()