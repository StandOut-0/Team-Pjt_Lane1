
# SQLAlchemy에서 SQL문을 안전하게 실행하기 위해 text를 가져온다.
from sqlalchemy import text


# db.py에 작성된 get_engine 함수를 가져온다.
# get_engine()은 MySQL 연결 객체를 만든다.
from map_db import get_engine, init_ev_station

init_ev_station()

# 크롤링 실행, MySQL 저장, MySQL 조회를 담당하는 서비스 클래스이다.
class MapService:
    # 객체가 생성될 때 실행되는 생성자이다.
    def __init__(self):
        # MySQL 연결 엔진을 생성한다.
        self.engine = get_engine()
       
    def selectEvStations(self, keyword: str = '') -> list:
        
        sql = """
        SELECT 
            stat_id, stat_nm, addr, addr_detail, lat, lng, busi_nm, busi_call,
            zscode, kind_detail, 
            case 
                when parking_free = 'Y' then '무료'
                else '유료' 
            end as parking_free,
            case
            	when use_time is null or use_time = '' then '알 수 없음'
            	else use_time
            end as use_time,
            limit_yn, charger_cnt, updated_at
        FROM
            ev_station_seoul
        WHERE
            addr like :addr
        or
            stat_nm like :stat_nm 
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), {"addr": f"%{keyword}%", "stat_nm" : f"%{keyword}%"})
            items = [dict(row._mapping) for row in result]
        return items

