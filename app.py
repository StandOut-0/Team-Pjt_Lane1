import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
from rightside import render_right_sidebar
from chat import render_chat_interface
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="서울에 ~한 충전소, 일차로",
    page_icon="docs/favicon_io/favicon.ico",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Dark mode styles */
    .dark-mode {
        --bg-primary: #1e1e1e;
        --bg-secondary: #2d2d2d;
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --border-color: #404040;
    }
    
    .light-mode {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --text-primary: #212529;
        --text-secondary: #6c757d;
        --border-color: #dee2e6;
    }
    
    /* Main container */
    .main-container {
        display: flex;
        height: 100vh;
        position: relative;
    }
    
    /* Left sidebar */
    .left-sidebar {
        width: 300px;
        background: var(--bg-secondary);
        padding: 20px;
        border-right: 1px solid var(--border-color);
        transition: width 0.3s ease;
    }
    
    .left-sidebar.collapsed {
        width: 60px;
    }
    
    /* Right sidebar */
    .right-sidebar {
        width: 300px;
        background: var(--bg-secondary);
        padding: 20px;
        border-left: 1px solid var(--border-color);
        transition: width 0.3s ease;
    }
    
    .right-sidebar.collapsed {
        width: 60px;
    }
    
    /* Logo area */
    .logo-area {
        text-align: center;
        padding: 20px 0;
        font-size: 24px;
        font-weight: bold;
        color: #1e88e5;
        border-bottom: 2px solid #1e88e5;
        margin-bottom: 20px;
    }
    
    /* Dark mode toggle button */
    .dark-mode-toggle {
        position: fixed;
        top: 70px;
        right: 20px;
        padding: 10px 15px;
        background: #1e88e5;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        z-index: 9999;
        font-size: 16px;
    }
    
    .dark-mode-toggle:hover {
        background: #1565c0;
    }
    
    /* Chat button */
    .chat-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: #1e88e5;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 24px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        z-index: 1000;
        transition: transform 0.2s;
    }
    
    .chat-button:hover {
        transform: scale(1.1);
    }
    
    /* Chat container */
    .chat-container {
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 350px;
        height: 500px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        z-index: 999;
        display: none;
        flex-direction: column;
    }
    
    .chat-container.open {
        display: flex;
    }
    
    .chat-container.fullscreen {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        width: 100vw;
        height: 100vh;
        border-radius: 0;
    }
    
    /* Chat header */
    .chat-header {
        padding: 15px;
        background: #1e88e5;
        color: white;
        border-radius: 10px 10px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .chat-container.fullscreen .chat-header {
        border-radius: 0;
    }
    
    /* Chat messages */
    .chat-messages {
        flex: 1;
        padding: 15px;
        overflow-y: auto;
    }
    
    /* Chat input */
    .chat-input {
        padding: 15px;
        border-top: 1px solid #dee2e6;
    }
    
    /* Map placeholder */
    .map-placeholder {
        height: 100%;
        background: var(--bg-secondary);
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        color: var(--text-secondary);
        font-size: 18px;
    }
    
    /* Dark mode body */
    body.dark-mode {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for UI controls
if 'left_sidebar_open' not in st.session_state:
    st.session_state.left_sidebar_open = True
if 'right_sidebar_open' not in st.session_state:
    st.session_state.right_sidebar_open = True
if 'chat_open' not in st.session_state:
    st.session_state.chat_open = False
if 'chat_fullscreen' not in st.session_state:
    st.session_state.chat_fullscreen = False
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Main layout - responsive based on right sidebar state
if st.session_state.right_sidebar_open:
    col1, col2 = st.columns([2, 1])
else:
    col1, col2 = st.columns([1, 0.1])

# Main Content (Dashboard)
with col1:
    st.markdown('<div class="logo-area">서울에 ~한 충전소, 일차로</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Dashboard graphs
    st.markdown("**대시보드**")
    
    # Sample data for graphs
    dates = pd.date_range(start='2024-01-01', periods=7, freq='D')
    values = [120, 150, 180, 220, 200, 250, 280]
    
    # Line chart
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers', name='충전량'))
    fig1.update_layout(title='일별 충전량', height=200)
    st.plotly_chart(fig1, width='stretch')
    
    # Bar chart
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=['강남구', '서초구', '송파구', '마포구', '영등포구'], 
                         y=[450, 380, 520, 290, 410], name='충전소 수'))
    fig2.update_layout(title='지역별 충전소 수', height=200)
    st.plotly_chart(fig2, width='stretch')
    
    # Pie chart
    fig3 = go.Figure()
    fig3.add_trace(go.Pie(labels=['전기차', '하이브리드', '기타'], 
                         values=[65, 25, 10], hole=0.3))
    fig3.update_layout(title='차량 유형 비율', height=200)
    st.plotly_chart(fig3, width='stretch')

# Right Sidebar (Map with search bar)
render_right_sidebar(col2)

# Dark mode toggle button
st.markdown(f"""
<button class="dark-mode-toggle" onclick="toggleDarkMode()">{'🌙' if not st.session_state.dark_mode else '☀️'}</button>

<script>
    function toggleDarkMode() {{
        document.body.classList.toggle('dark-mode');
    }}
</script>
""", unsafe_allow_html=True)

# Chat Interface (Floating)
render_chat_interface()

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center;color:#6c757d;'>© 2024 Map Application</div>", unsafe_allow_html=True)
