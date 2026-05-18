import streamlit as st


def render_left_sidebar(col):
    """Render the left sidebar with search and layer options"""
    with col:
        if st.session_state.left_sidebar_open:
            st.markdown('<div class="logo-area">서울에 ~한 충전소, 일차로</div>', unsafe_allow_html=True)
            st.markdown("---")
            
            # Search bar
            search_query = st.text_input("🔍 검색", placeholder="검색어를 입력하세요...")
            
            st.markdown("---")
            st.markdown("**레이어**")
            st.checkbox("도로", value=True, key="layer_road")
            st.checkbox("건물", value=True, key="layer_building")
            st.checkbox("위성", value=False, key="layer_satellite")
        
        # Toggle button for left sidebar
        if st.button("◀" if st.session_state.left_sidebar_open else "▶", key="left_toggle"):
            st.session_state.left_sidebar_open = not st.session_state.left_sidebar_open
            st.rerun()
