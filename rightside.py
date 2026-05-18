import streamlit as st


def render_right_sidebar():

    st.write("지도")

    if st.session_state.right_sidebar_open:

        # Search toggle block
        if st.button(
            "🔍 충전소 검색 열기"
            if not st.session_state.search_section_open
            else "🔽 충전소 검색 닫기",
            key="search_toggle"
        ):
            st.session_state.search_section_open = (
                not st.session_state.search_section_open
            )
            st.rerun()

        if st.session_state.search_section_open:

            search_query = st.text_input(
                "🔍 검색",
                value=st.session_state.search_query,
                placeholder="충전소, 지역 등을 검색하세요",
                key="search_query_input"
            )

            if st.button("검색", key="search_submit"):

                st.session_state.search_query = search_query

                st.session_state.search_results = [
                    f"{search_query} - 산출물 A",
                    f"{search_query} - 산출물 B",
                    f"{search_query} - 산출물 C"
                ]

            st.markdown("---")

        # Map area
        st.markdown(
            '<div class="map-placeholder">지도 영역 (API 연결 대기 중)</div>',
            unsafe_allow_html=True
        )

        if st.session_state.search_results:

            st.markdown('### 산출물 리스트')

            for result in st.session_state.search_results:
                st.markdown(f'- {result}')

    # Toggle button
    if st.button(
        "▶" if st.session_state.right_sidebar_open else "◀",
        key="right_toggle"
    ):

        st.session_state.right_sidebar_open = (
            not st.session_state.right_sidebar_open
        )

        st.rerun()