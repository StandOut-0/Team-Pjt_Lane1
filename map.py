import streamlit as st
import streamlit.components.v1 as components
from map_service import MapService

KAKAO_API_KEY = "c8c6db4376df95e5c6eedcd9140ffa19"


if "map_service" not in st.session_state:
    # CrawlService 객체를 처음 한 번만 생성해서 저장한다.
    st.session_state.map_service = MapService()

service = st.session_state.map_service

def render_map_area():
    
    """Render the main map area with placeholder"""
    
    # SAMPLE_DB = [
    #     {"stat_nm": "강남역 공영주차장 충전소",     "addr": "서울 강남구 강남대로 396",      "lat": 37.4979, "lng": 127.0276, "charger_cnt": 4},
    #     {"stat_nm": "강남구청 충전소",              "addr": "서울 강남구 학동로 426",         "lat": 37.5172, "lng": 127.0473, "charger_cnt": 2},
    #     {"stat_nm": "강남 세브란스병원 충전소",      "addr": "서울 강남구 언주로 211",         "lat": 37.5247, "lng": 127.0565, "charger_cnt": 3},
    #     {"stat_nm": "강남구 대치동 충전소",          "addr": "서울 강남구 대치동 316",         "lat": 37.5033, "lng": 127.0617, "charger_cnt": 6},
    #     {"stat_nm": "강남 파이낸스센터 충전소",      "addr": "서울 강남구 테헤란로 152",       "lat": 37.5001, "lng": 127.0363, "charger_cnt": 2},
    #     {"stat_nm": "서울시청 충전소",              "addr": "서울 중구 세종대로 110",          "lat": 37.5663, "lng": 126.9779, "charger_cnt": 3},
    #     {"stat_nm": "서울시청 지하주차장 충전소",    "addr": "서울 중구 세종대로 110 지하",    "lat": 37.5660, "lng": 126.9775, "charger_cnt": 5},
    #     {"stat_nm": "홍대입구역 충전소",            "addr": "서울 마포구 양화로 160",          "lat": 37.5572, "lng": 126.9249, "charger_cnt": 2},
    #     {"stat_nm": "홍대 공영주차장 충전소",        "addr": "서울 마포구 홍익로 3길 20",      "lat": 37.5566, "lng": 126.9238, "charger_cnt": 4},
    #     {"stat_nm": "광화문 충전소",               "addr": "서울 종로구 세종대로 172",         "lat": 37.5759, "lng": 126.9769, "charger_cnt": 2},
    #     {"stat_nm": "잠실역 충전소",               "addr": "서울 송파구 올림픽로 240",         "lat": 37.5133, "lng": 127.1001, "charger_cnt": 3},
    #     {"stat_nm": "잠실 롯데월드 충전소",         "addr": "서울 송파구 올림픽로 240",         "lat": 37.5110, "lng": 127.0980, "charger_cnt": 8},
    #     {"stat_nm": "코엑스 충전소",               "addr": "서울 강남구 봉은사로 524",         "lat": 37.5115, "lng": 127.0595, "charger_cnt": 6},
    # ]
    
    st.title("전기차 충전소 지도")
    
    
    # session_state 초기화
    if "search_results" not in st.session_state:
        st.session_state.search_results = []
    if "selected_idx" not in st.session_state:
        st.session_state.selected_idx = None
    
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("충전소 검색", placeholder="예: 강남, 홍대, 서울시청 ...")
    with col2:
        st.markdown('<div style="margin-top:28px;"></div>', unsafe_allow_html=True)
        search_btn = st.button("검색", use_container_width=True)
        
    if search_btn:
        if query:
            results = service.selectEvStations(query)
            # results = [s for s in SAMPLE_DB if query in s["stat_nm"] or query in s["addr"]]

            if not results:
                st.warning(f"'{query}'에 해당하는 충전소가 없습니다.")
                st.session_state.search_results = []
            elif len(results) > 50:
                st.warning(f"검색 결과가 너무 많습니다 ({len(results)}개). 더 구체적으로 입력해주세요.")
                st.session_state.search_results = []
            else:
                st.session_state.search_results = results
                st.session_state.selected_idx = None
        else:
            st.session_state.search_results = []
            st.session_state.selected_idx = None

    results = st.session_state.search_results
    selected_idx = st.session_state.selected_idx

    # 지도 중심 및 bounds 결정
    if results and selected_idx is not None:
        s = results[selected_idx]
        center_lat, center_lng, map_level = s["lat"], s["lng"], 4
        fit_bounds = False
    elif results:
        center_lat, center_lng, map_level = results[0]["lat"], results[0]["lng"], 8
        fit_bounds = True
    else:
        center_lat, center_lng, map_level = 37.5665, 126.9780, 8
        fit_bounds = False

    # 마커 JS 생성
    bounds_js = "var bounds = new kakao.maps.LatLngBounds();" if fit_bounds else ""
    set_bounds_js = "map.setBounds(bounds);" if fit_bounds and results else ""
    markers_js = ""

    for i, s in enumerate(results):
        is_selected = (selected_idx == i)
        open_iw = "infowindow.setContent(content); infowindow.open(map, marker);" if is_selected else ""
        extend = "bounds.extend(markerPos);" if fit_bounds else ""
        markers_js += f"""
        (function() {{
            var markerPos = new kakao.maps.LatLng({s['lat']}, {s['lng']});
            var marker = new kakao.maps.Marker({{ map: map, position: markerPos }});
            var content = '<div style="padding:6px;font-size:12px;min-width:160px; min-height:98px;">'
                + '<b>{s["stat_nm"]}</b><br>{s["addr"]}<br>충전기 {s["charger_cnt"]}대<br>이용가능시간 : {s["use_time"]}<br>주차요금 : {s["parking_free"]}</div>';
            {open_iw}
            kakao.maps.event.addListener(marker, 'click', function() {{
                infowindow.setContent(content);
                infowindow.open(map, marker);
            }});
            {extend}
        }})();
        """

    components.html(f"""
        <script src="//dapi.kakao.com/v2/maps/sdk.js?appkey={KAKAO_API_KEY}"></script>
        <div id="map" style="width:100%;height:560px;border-radius:8px;"></div>
        <script>
            var map = new kakao.maps.Map(document.getElementById('map'), {{
                center: new kakao.maps.LatLng({center_lat}, {center_lng}),
                level: {map_level}
            }});
            var infowindow = new kakao.maps.InfoWindow({{ zIndex: 1 }});
            kakao.maps.event.addListener(map, 'click', function() {{
                infowindow.close();
            }});
            {bounds_js}
            {markers_js}
            {set_bounds_js}
        </script>
    """, height=580)

    # 선택된 충전소 상세 정보
    if selected_idx is not None and results:
        s = results[selected_idx]
        st.info(f"**{s['stat_nm']}** | {s['addr']} | 충전기 {s['charger_cnt']}대 | 이용가능시간 : {s['use_time']} | 주차요금 : {s['parking_free']}")

    # 결과 목록 (지도 하단)
    if results:
        st.markdown(f"**검색 결과 {len(results)}개**")
        for i, station in enumerate(results):
            label = f"{'▶ ' if selected_idx == i else ''}{station['stat_nm']}"
            if st.button(label, key=f"s_{i}", use_container_width=True):
                st.session_state.selected_idx = i
                st.rerun()
    else:
        st.caption("검색 결과가 여기에 표시됩니다.")
        
    
    # with col:
    #     st.markdown('<div class="map-placeholder">지도 영역 (API 연결 대기 중)</div>', unsafe_allow_html=True)
