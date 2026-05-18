import requests
from urllib.parse import unquote
from sqlalchemy import text, create_engine
import os

SERVICE_KEY = "AdNZDr5s3Wzlh%2BB%2FzHMNCVsu8Z7SH6qH1MLVmEDcQ%2Fi7ZNvtm8C1%2F%2FEjAoxzrBRSrC%2BXS8W0m2AOGcP0rzV5xQ%3D%3D"
BASE_URL = "http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
NUM_OF_ROWS = 9999


def get_engine():
    # .env 파일에서 DB_HOST 값을 읽는다.
    # 값이 없으면 기본값으로 "localhost"를 사용한다.
    # localhost는 현재 내 컴퓨터를 의미한다.
    host = os.getenv("DB_HOST", "localhost")

    # .env 파일에서 DB_PORT 값을 읽는다.
    # 값이 없으면 MySQL 기본 포트인 "3306"을 사용한다.
    port = os.getenv("DB_PORT", "3306")

    # .env 파일에서 DB_USER 값을 읽는다.
    # 값이 없으면 기본값으로 "student"를 사용한다.
    user = os.getenv("DB_USER", "student")

    # .env 파일에서 DB_PASSWORD 값을 읽는다.
    # 값이 없으면 기본값으로 "Student80*"를 사용한다.
    password = os.getenv("DB_PASSWORD", "Student80*")

    # .env 파일에서 DB_NAME 값을 읽는다.
    # 값이 없으면 기본값으로 "mydb"를 사용한다.
    db_name = os.getenv("DB_NAME", "studentdb")

    # SQLAlchemy가 MySQL에 접속하기 위한 DB URL을 만든다.
    #
    # 형식:
    # mysql+pymysql://사용자명:비밀번호@호스트:포트/DB명?charset=utf8mb4
    #
    # mysql+pymysql:
    #   MySQL DB에 pymysql 드라이버를 사용해서 접속한다는 뜻이다.
    #
    # charset=utf8mb4:
    #   한글, 이모지, 특수문자까지 안정적으로 저장하기 위한 문자셋 설정이다.
    db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"

    # create_engine()은 DB 연결을 관리하는 엔진 객체를 만든다.
    #
    # pool_pre_ping=True:
    #   DB 연결을 사용하기 전에 연결이 살아 있는지 확인한다.
    #   오래된 연결이 끊겨서 발생하는 오류를 줄일 수 있다.
    return create_engine(db_url, pool_pre_ping=True)


CREATE_TABLE_SQL = text("""
CREATE TABLE IF NOT EXISTS ev_station_seoul (
    stat_id      VARCHAR(20)   NOT NULL         COMMENT '충전소ID (PK)',
    stat_nm      VARCHAR(100)                   COMMENT '충전소명',
    addr         VARCHAR(200)                   COMMENT '주소',
    addr_detail  VARCHAR(200)                   COMMENT '주소상세',
    lat          DECIMAL(15,7)                  COMMENT '위도',
    lng          DECIMAL(15,7)                  COMMENT '경도',
    use_time     VARCHAR(50)                    COMMENT '이용가능시간',
    busi_nm      VARCHAR(100)                   COMMENT '운영기관명',
    busi_call    VARCHAR(30)                    COMMENT '연락처',
    zscode       VARCHAR(5)                     COMMENT '시군구코드',
    kind_detail  VARCHAR(4)                     COMMENT '시설상세코드',
    parking_free CHAR(1)                        COMMENT '주차무료 (Y/N)',
    limit_yn     CHAR(1)                        COMMENT '이용제한 (Y/N)',
    charger_cnt  INT           DEFAULT 0        COMMENT '보유 충전기 수',
    updated_at   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (stat_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='서울시 전기차 충전소 (충전소 단위)'
""")

UPSERT_SQL = text("""
INSERT INTO ev_station_seoul
    (stat_id, stat_nm, addr, addr_detail, lat, lng, use_time,
     busi_nm, busi_call, zscode, kind_detail, parking_free, limit_yn, charger_cnt)
VALUES
    (:stat_id, :stat_nm, :addr, :addr_detail, :lat, :lng, :use_time,
     :busi_nm, :busi_call, :zscode, :kind_detail, :parking_free, :limit_yn, :charger_cnt)
ON DUPLICATE KEY UPDATE
    stat_nm     = VALUES(stat_nm),
    addr        = VALUES(addr),
    addr_detail = VALUES(addr_detail),
    lat         = VALUES(lat),
    lng         = VALUES(lng),
    busi_nm     = VALUES(busi_nm),
    charger_cnt = VALUES(charger_cnt)
""")


def _fetch(page):
    params = {
        "serviceKey": unquote(SERVICE_KEY),
        "pageNo": page,
        "numOfRows": NUM_OF_ROWS,
        "dataType": "JSON",
        "zcode": "11",
    }
    return requests.get(BASE_URL, params=params, timeout=30).json()


def _get_items(data):
    items = data.get("items", {}).get("item", [])
    if isinstance(items, dict):
        items = [items]
    return items


def _fetch_and_insert(conn):
    first = _fetch(1)
    total = first["totalCount"]
    total_pages = (total + NUM_OF_ROWS - 1) // NUM_OF_ROWS

    stations = {}
    charger_count = {}

    for item in _get_items(first):
        sid = item.get("statId")
        charger_count[sid] = charger_count.get(sid, 0) + 1
        if sid not in stations:
            stations[sid] = item

    for page in range(2, total_pages + 1):
        for item in _get_items(_fetch(page)):
            sid = item.get("statId")
            charger_count[sid] = charger_count.get(sid, 0) + 1
            if sid not in stations:
                stations[sid] = item

    rows = [
        {
            "stat_id":      sid,
            "stat_nm":      it.get("statNm"),
            "addr":         it.get("addr"),
            "addr_detail":  it.get("addrDetail"),
            "lat":          it.get("lat") or None,
            "lng":          it.get("lng") or None,
            "use_time":     it.get("useTime"),
            "busi_nm":      it.get("busiNm"),
            "busi_call":    it.get("busiCall"),
            "zscode":       it.get("zscode"),
            "kind_detail":  it.get("kindDetail"),
            "parking_free": it.get("parkingFree"),
            "limit_yn":     it.get("limitYn"),
            "charger_cnt":  charger_count[sid],
        }
        for sid, it in stations.items()
    ]

    conn.execute(UPSERT_SQL, rows)
    return len(rows)


def init_ev_station():
    """
    테이블이 없으면 생성하고, 데이터가 비어 있으면 API에서 가져와 삽입한다.
    이미 데이터가 있으면 아무것도 하지 않는다.
    """
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(CREATE_TABLE_SQL)
        count = conn.execute(text("SELECT COUNT(*) FROM ev_station_seoul")).scalar()

    if count == 0:
        with engine.begin() as conn:
            inserted = _fetch_and_insert(conn)
        print(f"[init_ev_station] 초기 데이터 삽입 완료: {inserted}개")
    else:
        print(f"[init_ev_station] 이미 데이터 존재 ({count}개), 건너뜀")
