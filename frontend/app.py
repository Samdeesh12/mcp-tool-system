# frontend/app.py
# This is the Streamlit web interface for our MCP Tool System.

import streamlit as st
import sys
import os

# This line makes sure Python can find our server/ and host/ folders
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from host.host import chat

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MCP Intelligent Tool System",
    page_icon="🤖",
    layout="wide"
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .tool-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 2px;
    }
    .user-message {
        background: #e3f2fd;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #1976d2;
    }
    .assistant-message {
        background: #f3e5f5;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #7b1fa2;
    }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
# Session state persists data across reruns (when user sends a message)
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "chat_display" not in st.session_state:
    st.session_state.chat_display = []  # For displaying messages in the UI

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛠️ Available Tools")
    st.markdown("""
    | Tool | What it does |
    |------|-------------|
    | 🌤️ Weather | Get live weather for any city |
    | 💱 Currency | Convert between currencies |
    | 📰 News | Latest headlines on any topic |
    | 😊 Sentiment | Analyze text emotion |
    | 💰 Expenses | Add and track expenses |
    """)

    st.markdown("---")
    st.markdown("## 💡 Try asking:")
    examples = [
        "What's the weather in Delhi?",
        "Convert 500 EUR to INR",
        "Latest news on AI",
        "Analyze: This project is amazing!",
        "Add expense: 200 for food today",
        "Show my expenses this month"
    ]
    for ex in examples:
        if st.button(ex, key=ex, use_container_width=True):
            st.session_state.pending_query = ex

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.conversation_history = []
        st.session_state.chat_display = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    st.metric("Messages sent", len(st.session_state.chat_display))

# ─── MAIN AREA ────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🤖 MCP Intelligent Tool System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by Groq AI + Model Context Protocol</div>', unsafe_allow_html=True)

# Display conversation history
chat_container = st.container()
with chat_container:
    for msg in st.session_state.chat_display:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message">👤 <strong>You:</strong> {msg["content"]}</div>',
                       unsafe_allow_html=True)
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["content"])

# ─── CHAT INPUT ───────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask anything — weather, news, currency, sentiment, expenses...")

# Handle sidebar example button clicks
if "pending_query" in st.session_state:
    user_input = st.session_state.pending_query
    del st.session_state.pending_query

# Process the message
if user_input:
    # Show user message immediately
    st.session_state.chat_display.append({
        "role": "user",
        "content": user_input
    })

    # Show a spinner while the AI thinks
    with st.spinner("🤖 Thinking and calling tools..."):
        try:
            response = chat(user_input, st.session_state.conversation_history)
        except Exception as e:
            response = f"Sorry, something went wrong: {str(e)}"

    # Add AI response to display
    st.session_state.chat_display.append({
        "role": "assistant",
        "content": response
    })

    # Rerun to update the UI
    st.rerun()