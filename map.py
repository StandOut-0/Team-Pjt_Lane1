import streamlit as st


def render_map_area(col):
    """Render the main map area with placeholder"""
    with col:
        st.markdown('<div class="map-placeholder">지도 영역 (API 연결 대기 중)</div>', unsafe_allow_html=True)
