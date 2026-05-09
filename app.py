import os
import html
import textwrap
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

st.set_page_config(
    page_title="WriteWise AI",
    page_icon="W",
    layout="centered",
    initial_sidebar_state="collapsed"
)

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    st.error("GEMINI_API_KEY belum ditemukan. Isi file .env dulu.")
    st.stop()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config={
        "temperature": 0.45,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 1200,
    },
    system_instruction="""
You are WriteWise AI, an English grammar chatbot.

Your job:
- correct English grammar
- improve sentence clarity
- rewrite sentences naturally
- explain grammar mistakes
- answer grammar questions

Rules:
- Use friendly but professional English.
- If user writes in Indonesian, explain in Indonesian.
- Keep answers clear and useful.
- Format answers neatly.
- Avoid overly long answers unless the user asks for detailed explanation.
"""
)


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

html {
    scroll-behavior: smooth;
}

.stApp {
    background:
        radial-gradient(circle at 12% 8%, rgba(96, 165, 250, 0.26), transparent 28%),
        radial-gradient(circle at 88% 16%, rgba(124, 58, 237, 0.22), transparent 30%),
        radial-gradient(circle at 70% 92%, rgba(168, 85, 247, 0.18), transparent 34%),
        linear-gradient(135deg, #050816 0%, #0B1022 45%, #140B2E 100%);
    color: #F8FAFC;
}

[data-testid="stHeader"] {
    display: none;
}

[data-testid="stToolbar"] {
    display: none;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    max-width: 1040px;
    padding-top: 3.2rem;
    padding-bottom: 4rem;
}

.hero {
    text-align: center;
    margin-bottom: 28px;
}

.logo {
    width: 72px;
    height: 72px;
    margin: 0 auto 18px;
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        linear-gradient(135deg, rgba(96, 165, 250, 1), rgba(124, 58, 237, 1));
    color: white;
    font-size: 32px;
    font-weight: 900;
    box-shadow:
        0 24px 60px rgba(99, 102, 241, 0.36),
        inset 0 1px 0 rgba(255, 255, 255, 0.32);
}

.hero h1 {
    color: #FFFFFF;
    font-size: clamp(42px, 7vw, 68px);
    line-height: 1;
    letter-spacing: -2.8px;
    font-weight: 900;
    margin: 0;
}

.hero p {
    max-width: 720px;
    margin: 18px auto 0;
    color: #B9C4E2;
    font-size: 17px;
    line-height: 1.75;
}

.hero-chips {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 22px;
}

.hero-chip {
    color: #DDE6FF;
    font-size: 13px;
    font-weight: 700;
    padding: 9px 14px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.075);
    border: 1px solid rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(14px);
}


.chat-panel {
    width: 100%;
    margin: 0 auto 22px;
    padding: 26px;
    border-radius: 34px;
    background:
        linear-gradient(135deg, rgba(255, 255, 255, 0.105), rgba(255, 255, 255, 0.045));
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow:
        0 30px 90px rgba(0, 0, 0, 0.36),
        inset 0 1px 0 rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(22px);
}

.chat-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 24px;
    padding-bottom: 18px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.09);
}

.chat-title {
    display: flex;
    align-items: center;
    gap: 12px;
}

.status-dot {
    width: 12px;
    height: 12px;
    border-radius: 999px;
    background: #22C55E;
    box-shadow: 0 0 0 6px rgba(34, 197, 94, 0.12);
}

.chat-title strong {
    display: block;
    color: #FFFFFF;
    font-size: 15px;
}

.chat-title span {
    display: block;
    color: #AEB9D7;
    font-size: 13px;
    margin-top: 2px;
}

.chat-pill {
    color: #C7D2FE;
    font-size: 12px;
    font-weight: 800;
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(99, 102, 241, 0.16);
    border: 1px solid rgba(165, 180, 252, 0.16);
}

.message-row {
    display: flex;
    align-items: flex-end;
    gap: 14px;
    margin-bottom: 18px;
    animation: fadeInUp 0.24s ease both;
}

.message-row.user {
    flex-direction: row-reverse;
}

.avatar {
    width: 44px;
    height: 44px;
    border-radius: 16px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 13px;
    letter-spacing: -0.3px;
}

.avatar.bot {
    color: white;
    background: linear-gradient(135deg, #60A5FA, #7C3AED);
    box-shadow: 0 16px 34px rgba(124, 58, 237, 0.30);
}

.avatar.user {
    color: #E5E7EB;
    background: rgba(255, 255, 255, 0.11);
    border: 1px solid rgba(255, 255, 255, 0.16);
}

.bubble {
    max-width: min(760px, 78%);
    padding: 17px 20px;
    border-radius: 25px;
    font-size: 15.5px;
    line-height: 1.75;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

.bubble.bot {
    color: #F8FAFC;
    background: rgba(255, 255, 255, 0.095);
    border: 1px solid rgba(255, 255, 255, 0.13);
    border-bottom-left-radius: 9px;
}

.bubble.user {
    color: #FFFFFF;
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    border-bottom-right-radius: 9px;
    box-shadow: 0 18px 40px rgba(37, 99, 235, 0.25);
}

.quick-area {
    margin-top: 26px;
}

.quick-heading {
    color: #E8EEFF;
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 12px;
}

.quick-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
}

.quick-card {
    padding: 18px;
    min-height: 102px;
    border-radius: 24px;
    background:
        linear-gradient(135deg, rgba(255, 255, 255, 0.095), rgba(255, 255, 255, 0.04));
    border: 1px solid rgba(255, 255, 255, 0.12);
    transition: 0.2s ease;
}

.quick-card:hover {
    transform: translateY(-2px);
    border-color: rgba(165, 180, 252, 0.42);
    background: rgba(255, 255, 255, 0.105);
}

.quick-card strong {
    display: block;
    color: #FFFFFF;
    font-size: 15px;
    margin-bottom: 8px;
}

.quick-card span {
    color: #C6D0EA;
    font-size: 14px;
    line-height: 1.6;
}


.composer-label {
    margin: 26px 0 12px;
    color: #E8EEFF;
    font-size: 15px;
    font-weight: 900;
}

div[data-testid="stForm"] {
    padding: 20px !important;
    border-radius: 30px !important;
    background:
        linear-gradient(135deg, rgba(15, 23, 42, 0.82), rgba(30, 41, 59, 0.68)) !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    box-shadow:
        0 24px 80px rgba(0, 0, 0, 0.34),
        inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(18px);
}

div[data-testid="stTextArea"] textarea {
    min-height: 112px !important;
    max-height: 240px !important;
    padding: 18px 20px !important;
    border-radius: 23px !important;
    background: rgba(255, 255, 255, 0.085) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    box-shadow: none !important;
    font-size: 16px !important;
    line-height: 1.6 !important;
    resize: vertical !important;
}

div[data-testid="stTextArea"] textarea::placeholder {
    color: rgba(226, 232, 240, 0.55) !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(129, 140, 248, 0.92) !important;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.20) !important;
}

div[data-testid="stFormSubmitButton"] button {
    height: 56px !important;
    border-radius: 19px !important;
    border: 0 !important;
    color: #FFFFFF !important;
    font-weight: 900 !important;
    font-size: 15px !important;
    background: linear-gradient(135deg, #3B82F6, #7C3AED) !important;
    box-shadow: 0 18px 38px rgba(79, 70, 229, 0.34) !important;
    transition: 0.2s ease !important;
}

div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 22px 44px rgba(79, 70, 229, 0.42) !important;
}

.helper-note {
    margin-top: 14px;
    color: #97A6C8;
    font-size: 13px;
    line-height: 1.65;
    text-align: center;
}

.stAlert {
    border-radius: 18px;
}

[data-testid="stSpinner"] {
    color: #C7D2FE;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(7px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (max-width: 760px) {
    .block-container {
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero h1 {
        letter-spacing: -1.8px;
    }

    .hero p {
        font-size: 15px;
    }

    .chat-panel {
        padding: 18px;
        border-radius: 28px;
    }

    .chat-top {
        align-items: flex-start;
        flex-direction: column;
    }

    .quick-grid {
        grid-template-columns: 1fr;
    }

    .bubble {
        max-width: 84%;
        font-size: 14.5px;
    }

    .avatar {
        width: 39px;
        height: 39px;
        border-radius: 14px;
    }

    div[data-testid="stForm"] {
        padding: 16px !important;
        border-radius: 25px !important;
    }

    div[data-testid="stTextArea"] textarea {
        min-height: 104px !important;
    }
}
</style>
""",
    unsafe_allow_html=True
)


def render_html(block: str) -> None:
    clean_block = textwrap.dedent(block).strip()
    st.markdown(clean_block, unsafe_allow_html=True)


def safe_text(value: str) -> str:
    return html.escape(str(value))


def ask_ai(user_message: str) -> str:
    history_text = ""

    for msg in st.session_state.messages[-8:]:
        role = "User" if msg["role"] == "user" else "WriteWise"
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""
Conversation history:
{history_text}

Current user message:
{user_message}

Respond as WriteWise AI.

If the user gives an English sentence:
1. Give the corrected version.
2. Give a more natural version if useful.
3. Briefly explain what changed.

If the user asks a grammar question:
Answer clearly and practically.
"""

    response = model.generate_content(prompt)

    try:
        text = response.text
    except Exception:
        text = ""

    if not text or not text.strip():
        return "Sorry, I could not generate a response. Please try again."

    return text.strip()


def build_message_html(role: str, content: str) -> str:
    escaped_content = safe_text(content)

    if role == "user":
        return (
            '<div class="message-row user">'
            '<div class="avatar user">YOU</div>'
            f'<div class="bubble user">{escaped_content}</div>'
            '</div>'
        )

    return (
        '<div class="message-row bot">'
        '<div class="avatar bot">W</div>'
        f'<div class="bubble bot">{escaped_content}</div>'
        '</div>'
    )


def build_quick_cards_html() -> str:
    cards = [
        ("Grammar Fix", "i goes to school yesterday"),
        ("Make it formal", "can u help me with this?"),
        ("Improve paragraph", "Paste your paragraph and ask WriteWise to polish it."),
        ("Explain grammar", "Ask why a sentence sounds wrong."),
    ]

    html_cards = ""
    for title, example in cards:
        html_cards += (
            '<div class="quick-card">'
            f'<strong>{safe_text(title)}</strong>'
            f'<span>{safe_text(example)}</span>'
            '</div>'
        )

    return (
        '<div class="quick-area">'
        '<div class="quick-heading">Try these examples</div>'
        '<div class="quick-grid">'
        f'{html_cards}'
        '</div>'
        '</div>'
    )


def build_chat_panel_html() -> str:
    panel = (
        '<section class="chat-panel">'
        '<div class="chat-top">'
        '<div class="chat-title">'
        '<div class="status-dot"></div>'
        '<div>'
        '<strong>WriteWise is ready</strong>'
        '<span>Grammar correction, smoother wording, and clearer explanations.</span>'
        '</div>'
        '</div>'
        '<div class="chat-pill">English Assistant</div>'
        '</div>'
    )

    for msg in st.session_state.messages:
        panel += build_message_html(msg["role"], msg["content"])

    if len(st.session_state.messages) == 1:
        panel += build_quick_cards_html()

    panel += '</section>'
    return panel


def submit_message(user_text: str) -> None:
    st.session_state.messages.append({
        "role": "user",
        "content": user_text
    })

    with st.spinner("WriteWise is polishing your sentence..."):
        try:
            reply = ask_ai(user_text)
        except Exception as error:
            reply = f"Sorry, something went wrong while generating the response. Error: {error}"

    st.session_state.messages.append({
        "role": "bot",
        "content": reply
    })


WELCOME_MESSAGE = (
    "Hi, I'm WriteWise AI. Paste any English sentence or paragraph, "
    "and I'll help you correct the grammar, improve the wording, "
    "and explain what changed."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "bot",
            "content": WELCOME_MESSAGE
        }
    ]

render_html(
    """
    <div class="hero">
        <div class="logo">W</div>
        <h1>WriteWise AI</h1>
        <p>Your English grammar chatbot for clearer, smoother, and more natural writing.</p>
        <div class="hero-chips">
            <div class="hero-chip">Grammar Fix</div>
            <div class="hero-chip">Natural Rewrite</div>
            <div class="hero-chip">Formal Tone</div>
            <div class="hero-chip">Simple Explanation</div>
        </div>
    </div>
    """
)

render_html(build_chat_panel_html())

render_html('<div class="composer-label">Write your sentence</div>')

with st.form("writewise_form", clear_on_submit=True):
    user_input = st.text_area(
        label="Message",
        placeholder="Example: i goes to school yesterday",
        label_visibility="collapsed",
        height=112
    )

    submitted = st.form_submit_button(
        "Send",
        use_container_width=True
    )

if submitted:
    cleaned_input = user_input.strip()

    if cleaned_input:
        submit_message(cleaned_input)
        st.rerun()
    else:
        st.warning("Tulis kalimat dulu ya.")

render_html(
    """
    <div class="helper-note">
        Tip: Try typing <b>i goes to school yesterday</b> or 
        <b>make this sentence more professional: can u help me?</b>
    </div>
    """
)