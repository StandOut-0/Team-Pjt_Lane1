import streamlit as st


def render_chat_interface():
    """Render the floating chat interface with bot functionality"""
    st.markdown("""
<button class="chat-button" onclick="toggleChat()">💬</button>
<div class="chat-container" id="chatContainer">
    <div class="chat-header">
        <span>챗봇</span>
        <div>
            <button onclick="toggleFullscreen()" style="background:none;border:none;color:white;cursor:pointer;margin-right:10px;">⛶</button>
            <button onclick="toggleChat()" style="background:none;border:none;color:white;cursor:pointer;">✕</button>
        </div>
    </div>
    <div class="chat-messages" id="chatMessages">
        <div style="margin-bottom:10px;"><strong>챗봇:</strong> 안녕하세요! 무엇을 도와드릴까요?</div>
    </div>
    <div class="chat-input">
        <input type="text" id="chatInput" placeholder="메시지를 입력하세요..." style="width:100%;padding:8px;border:1px solid #dee2e6;border-radius:4px;" onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()" style="width:100%;margin-top:10px;padding:8px;background:#1e88e5;color:white;border:none;border-radius:4px;cursor:pointer;">전송</button>
    </div>
</div>

<script>
    function toggleChat() {
        const container = document.getElementById('chatContainer');
        container.classList.toggle('open');
    }
    
    function toggleFullscreen() {
        const container = document.getElementById('chatContainer');
        container.classList.toggle('fullscreen');
    }
    
    function sendMessage() {
        const input = document.getElementById('chatInput');
        const messages = document.getElementById('chatMessages');
        const text = input.value.trim();
        
        if (text) {
            messages.innerHTML += '<div style="margin-bottom:10px;text-align:right;"><strong>사용자:</strong> ' + text + '</div>';
            input.value = '';
            
            // Simulate bot response
            setTimeout(() => {
                messages.innerHTML += '<div style="margin-bottom:10px;"><strong>챗봇:</strong> 메시지를 받았습니다: ' + text + '</div>';
                messages.scrollTop = messages.scrollHeight;
            }, 500);
            
            messages.scrollTop = messages.scrollHeight;
        }
    }
    
    function handleKeyPress(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    }
</script>
""", unsafe_allow_html=True)
