import streamlit as st
import map 

def render_right_sidebar(col):
    """Render the right sidebar with map area"""
    with col:
        # Toggle button for right sidebar
        if st.button("▶" if st.session_state.right_sidebar_open else "◀", key="right_toggle"):
            st.session_state.right_sidebar_open = not st.session_state.right_sidebar_open
            st.rerun()

        if st.session_state.right_sidebar_open:
            # Search bar above map
            # search_query = st.text_input("🔍 검색", placeholder="충전소, 지역 등을 검색하세요")

            # st.markdown("---")

            # Map area
            # st.markdown('<div class="map-placeholder">지도 영역 (API 연결 대기 중)</div>', unsafe_allow_html=True)
            map.render_map_area(col)
