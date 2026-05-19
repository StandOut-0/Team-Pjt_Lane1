from sqlalchemy import text
from db import get_engine
import pandas as pd


class CarService:
    def __init__(self):
        # MySQL 연결 엔진을 생성한다.
        self.engine = get_engine()
        
    def selectConstituencyGroupList(self, keyword: str = '') -> list:
        sql = """
        SELECT
            REGEXP_SUBSTR(addr, '[^ ]+구') AS district,
            COUNT(*) AS cnt
        FROM ev_station_seoul
        GROUP BY REGEXP_SUBSTR(addr, '[^ ]+구')
        HAVING district IS NOT NULL
        ORDER BY cnt DESC
        """
        # return pd.read_sql(sql, self.engine)
        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            items = [dict(row._mapping) for row in result]
        return items
    
    def selectCarCategoryList(self, keyword: str= '') -> list:
        sql = """
        SELECT
            ROUND(gasCar / totalCar * 100, 1) AS gasCarPct,
            ROUND(elecCar / totalCar * 100, 1) AS elecCarPct
        FROM (
            SELECT
                avg(t1.seoul) AS totalCar,
                avg(t1.seoul - t2.seoul) AS gasCar,
                avg(t2.seoul) AS elecCar
            FROM ev_car_ratio t1
            LEFT JOIN ev_car t2 ON t1.date = t2.date
        ) sub
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            items = [dict(row._mapping) for row in result]
        return items
        
        
    def selectCarYOYList(self, keyword : str = '') -> list:
        sql = """
            SELECT 
                t1.seoul
            from 
                ev_car t1
            where
                t1.date between '2025-01' and '2025-10'
        """
        
        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            # items1 = [dict(row._mapping) for row in result]
            items1 = [row[0] for row in result]
        
        sql2 = """
            SELECT 
                t1.seoul
            from 
                ev_car t1
            where
                t1.date between '2024-01' and '2024-10'
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(sql2))
            # items2 = [dict(row._mapping) for row in result]
            items2 = [row[0] for row in result]
            items ={'table1' : items1, 'table2' : items2}
        return items
            
            