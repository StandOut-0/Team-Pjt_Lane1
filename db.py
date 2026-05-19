import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text 
import glob
import pandas as pd

# 현재 프로젝트 폴더의 .env 파일을 읽어온다.
load_dotenv()

def get_engine():
    host = os.getenv("DB_HOST")

    # .env 파일에서 DB_PORT 값을 읽는다.
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"
    return create_engine(db_url, pool_pre_ping=True)

# 크롤링 데이터를 저장할 테이블을 생성하는 함수이다.
def init_table():
    engine = get_engine()   
    
    sql_1 = """
    CREATE TABLE IF NOT EXISTS ev_car (
        `date` 	VARCHAR(10) PRIMARY KEY COMMENT '날짜',
        `seoul` 	INT	NOT NULL COMMENT '전기차 등록 개수'
        ); 
    """

    sql_2 = """
    CREATE TABLE IF NOT EXISTS ev_car_ratio (
        `date` 	VARCHAR(10) PRIMARY KEY COMMENT '날짜',
        `seoul` 	INT	NOT NULL COMMENT '내연+전기차 등록 개수'
        ); 
    """

    with engine.begin() as conn:
        # text(sql)은 문자열 SQL을 실행 가능한 SQLAlchemy SQL 객체로 변환한다.
        # conn.execute()는 실제로 SQL문을 DB에 실행한다.
        conn.execute(text(sql_1))
        conn.execute(text(sql_2))
        # insert 데이터 호출
        insert_ev_ratio_data()
        insert_ev_car_data()


# 데이터 insert 하는 코드

# 1. ev_car 테이블에 엑셀 데이터 삽입 (pandas 활용)
def insert_ev_car_data():
    engine = get_engine()
    
    file_candidates = glob.glob(os.path.join("raw_data", "*전기차등록현황.xlsx"))
    if not file_candidates:
        print("❌ 전기차 등록현황 엑셀 파일을 찾을 수 없습니다.")
        return
        
    excel_path = file_candidates[0]
    print(f"🚀 전기차 등록현황 데이터 삽입 중... ({os.path.basename(excel_path)})")
    
    # 📌 [반영] 5행부터 데이터 시작이므로, 4행에 있는 헤더를 읽기 위해 header=3 지정 (0부터 시작하므로)
    df = pd.read_excel(excel_path, header=3)
    
    # 안전하게 앞의 2개 열('년월', '서울')만 선택하여 구조 고정
    df = df.iloc[:, :2]
    df.columns = ['date', 'seoul']
    
    # 데이터 전처리 (공백 제거 및 숫자 변환)
    df['date'] = df['date'].astype(str).str.strip()
    df['seoul'] = pd.to_numeric(df['seoul'], errors='coerce').fillna(0).astype(int)
    
    # 6. 기본키 중복 방지를 위한 기존 데이터 초기화 (TRUNCATE)
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE ev_car;"))
    
    # DB에 삽입
    df.to_sql(name='ev_car', con=engine, if_exists='append', index=False)
    print(f"✅ ev_car 테이블에 {len(df)}건의 데이터 삽입 완료!")


# 2. ev_car_ratio 테이블에 KOSIS 엑셀 데이터 삽입
def insert_ev_ratio_data():
    engine = get_engine()
    
    file_candidates = glob.glob(os.path.join("raw_data", "*KOSIS_자동차등록대수현황.xlsx"))
    if not file_candidates:
        print("❌ KOSIS 자동차등록대수현황 엑셀 파일을 찾을 수 없습니다.")
        return
        
    excel_path = file_candidates[0]
    print(f"🚀 KOSIS 자동차 등록 비율 데이터 삽입 중... ({os.path.basename(excel_path)})")
    
    # 📌 [반영] 1행이 '시점, 서울' 헤더이므로 header=0으로 읽은 뒤, 
    # 3행부터 데이터가 시작되므로 2행(총합 행, 인덱스 0번)을 자릅니다.
    df = pd.read_excel(excel_path, header=0)
    df = df.iloc[1:]  # 2번째 행 제거하여 3번째 행부터 남김
    
    # 중복된 컬럼명이나 서식 문제를 방지하기 위해 위치(순서) 기반으로 앞의 2개 열만 선택
    df = df.iloc[:, :2]
    df.columns = ['date', 'seoul']
    
    # 데이터 전처리 (공백 제거 및 숫자 변환)
    df['date'] = df['date'].astype(str).str.strip()
    
    # 💡 [PM의 데이터 팁] 
    # KOSIS 파일의 날짜는 '2025.10' 형태이고, 전기차 현황은 '2025-10' 형태입니다.
    # 나중에 두 테이블을 날짜 기준으로 JOIN해서 비율을 편하게 계산할 수 있도록 하이픈(-)으로 통일해 줍니다.
    df['date'] = df['date'].str.replace('.', '-', regex=False)
    
    df['seoul'] = pd.to_numeric(df['seoul'], errors='coerce').fillna(0).astype(int)
    
    # 기본키 중복 방지를 위한 기존 데이터 초기화 (TRUNCATE)
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE ev_car_ratio;"))
    
    # DB에 삽입
    df.to_sql(name='ev_car_ratio', con=engine, if_exists='append', index=False)
    print(f"✅ ev_car_ratio 테이블에 {len(df)}건의 데이터 삽입 완료!")


# --- 한 번에 순서대로 실행해주는 마스터 마이그레이션 함수 ---
def main_migration():
    print("====== 🌟 데이터베이스 적재(Migration) 시작 ======")
    
    # 1단계: 필요하다면 테이블부터 생성/초기화 (앞서 고친 함수)
    init_table() 
    
    # 2단계: 데이터 각각 채워 넣기        
    try:
        insert_ev_car_data()
    except Exception as e:
        print(f"⚠️ 전기차 등록현황 데이터 적재 중 오류 발생: {e}")
        
    try:
        insert_ev_ratio_data()
    except Exception as e:
        print(f"⚠️ KOSIS 등록비율 데이터 적재 중 오류 발생: {e}")
        
    print("====== 🏁 모든 데이터 마이그레이션 작업 종료 ======")