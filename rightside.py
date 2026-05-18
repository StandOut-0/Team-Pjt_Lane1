import streamlit as st
import map


def render_right_sidebar():
    """Render the right sidebar with map area"""

    # Toggle button for right sidebar
    if st.button(
        "▶" if st.session_state.right_sidebar_open else "◀",
        key="right_toggle"
    ):

        st.session_state.right_sidebar_open = (
            not st.session_state.right_sidebar_open
        )

        st.rerun()

    if st.session_state.right_sidebar_open:

        map.render_map_area()