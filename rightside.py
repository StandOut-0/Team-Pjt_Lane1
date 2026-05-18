import streamlit as st


def render_right_sidebar(col):
    """Render the right sidebar with information panel"""
    with col:
        if st.session_state.right_sidebar_open:
            st.markdown("**정보 패널**")
            st.markdown("---")
            st.markdown("선택한 위치의 정보가 여기에 표시됩니다.")
        
        # Toggle button for right sidebar
        if st.button("▶" if st.session_state.right_sidebar_open else "◀", key="right_toggle"):
            st.session_state.right_sidebar_open = not st.session_state.right_sidebar_open
            st.rerun()
