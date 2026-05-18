import streamlit.components.v1 as components
import json
import os


def render_chat_interface():
    # Load FAQ data
    faq_data = []
    try:
        with open('faq_data.json', 'r', encoding='utf-8') as f:
            faq_data = json.load(f)
    except FileNotFoundError:
        print("FAQ data file not found")
    except Exception as e:
        print(f"Error loading FAQ data: {e}")

    # Convert FAQ data to JavaScript
    faq_js = json.dumps(faq_data, ensure_ascii=False)
    
    chat_html = """
    # <!DOCTYPE html>
    # <html>
    # <head>
    <style>

    .chat-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 65px;
        height: 65px;
        border-radius: 50%;
        background-color: #1e88e5;
        color: white;
        border: none;
        font-size: 28px;
        cursor: pointer;
        z-index: 9999;

        position: fixed;
        bottom: 20px;
        right: 20px;
    }

    .chat-container {
        display: none;
        position: fixed;
        bottom: 100px;
        right: 20px;
        width: 350px;
        height: 500px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        overflow: hidden;
        z-index: 9999;
        flex-direction: column;
    }

    .chat-header {
        background: #1e88e5;
        color: white;
        padding: 15px;
        font-weight: bold;
    }

    .chat-messages {
        flex: 1;
        padding: 10px;
        overflow-y: auto;
        height: 350px;
    }

    .chat-input {
        padding: 10px;
        border-top: 1px solid #ddd;
    }

    .chat-input input {
        width: 95%;
        padding: 10px;
    }

    .open {
        display: flex;
    }

    </style>
    # </head>

    # <body>

    <button class="chat-button" onclick="toggleChat()">
        💬
    </button>

    <div class="chat-container" id="chatContainer">

        <div class="chat-header">
            EV 챗봇
        </div>

        <div class="chat-messages" id="chatMessages">
            <div><b>챗봇:</b> 안녕하세요! 질문해주세요.</div>
        </div>

        <div class="chat-input">
            <input
                type="text"
                id="userInput"
                placeholder="질문 입력..."
                onkeypress="handleKey(event)"
            >
        </div>

    </div>

    <script>

    const faqData = """ + faq_js + """;

    function toggleChat() {
        const chat = document.getElementById("chatContainer");
        chat.classList.toggle("open");
    }

    function findAnswer(question) {
        const lowerQuestion = question.toLowerCase();
        let bestMatch = null;
        let highestScore = 0;

        for (const faq of faqData) {
            let score = 0;
            const lowerTitle = faq.title.toLowerCase();
            const lowerAnswer = faq.answer.toLowerCase();

            // Check for exact keyword matches
            const keywords = lowerQuestion.split(' ').filter(word => word.length > 1);
            
            for (const keyword of keywords) {
                if (lowerTitle.includes(keyword)) {
                    score += 2;
                }
                if (lowerAnswer.includes(keyword)) {
                    score += 1;
                }
            }

            // Bonus for longer matches
            if (lowerTitle.includes(lowerQuestion) || lowerQuestion.includes(lowerTitle)) {
                score += 5;
            }

            if (score > highestScore) {
                highestScore = score;
                bestMatch = faq;
            }
        }

        if (highestScore > 0) {
            return bestMatch.answer;
        }
        return "죄송합니다. 해당 질문에 대한 답변을 찾지 못했습니다. 다른 질문을 해주세요.";
    }

    function handleKey(event) {

        if(event.key === "Enter") {

            const input = document.getElementById("userInput");
            const text = input.value;

            if(text.trim() === "") return;

            const messages = document.getElementById("chatMessages");

            messages.innerHTML += `
                <div style="text-align:right; margin:10px 0;">
                    <b>사용자:</b> ${text}
                </div>
            `;

            const response = findAnswer(text);

            messages.innerHTML += `
                <div style="margin:10px 0;">
                    <b>챗봇:</b> ${response}
                </div>
            `;

            input.value = "";

            messages.scrollTop = messages.scrollHeight;
        }
    }

    </script>

    # </body>
    # </html>
    """

    components.html(chat_html, height=600)