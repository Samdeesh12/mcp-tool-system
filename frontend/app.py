# frontend/app.py

import streamlit as st
import sys, os, re
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from host.host import chat
from frontend.utils.logger import log_conversation

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MCP Tool System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CLEAN AI RESPONSE ─────────────────────────────────────────────────────────
def clean_response(text: str) -> str:
    text = re.sub(r'<(?!(?:br|b|i|strong|em|ul|ol|li|p|h[1-6]|code|pre)\b)[^>]+>', '', text)
    return text.strip()

# ── CSS — split into small injections to prevent Streamlit rendering bug ──────
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">', unsafe_allow_html=True)
st.markdown("<style>:root{--bg:#080c14;--bg2:#0e1623;--bg3:#151f2e;--border:rgba(255,255,255,0.07);--accent:#00d4ff;--text:#e2e8f0;--muted:#64748b;}</style>", unsafe_allow_html=True)
st.markdown("<style>html,body,[class*='css']{font-family:'DM Sans',sans-serif !important;background:#080c14 !important;color:#e2e8f0 !important;}#MainMenu,footer,header{visibility:hidden;}</style>", unsafe_allow_html=True)
st.markdown("<style>.block-container{padding:1.5rem 2rem 5rem 2rem !important;max-width:860px !important;margin:0 auto !important;}[data-testid='stAppViewContainer']{background:#080c14 !important;}</style>", unsafe_allow_html=True)
st.markdown("<style>[data-testid='stSidebar']{background:#0e1623 !important;border-right:1px solid rgba(255,255,255,0.07) !important;}section[data-testid='stSidebar'] *{color:#e2e8f0 !important;}</style>", unsafe_allow_html=True)
st.markdown("<style>[data-testid='stSidebar'] .stButton>button{background:#151f2e !important;border:1px solid rgba(255,255,255,0.07) !important;color:#94a3b8 !important;border-radius:8px !important;font-size:0.78rem !important;text-align:left !important;width:100% !important;padding:7px 12px !important;font-family:'DM Sans',sans-serif !important;transition:all 0.15s;}[data-testid='stSidebar'] .stButton>button:hover{border-color:#00d4ff !important;color:#00d4ff !important;background:rgba(0,212,255,0.05) !important;}</style>", unsafe_allow_html=True)
st.markdown("<style>[data-testid='stMetric']{background:#151f2e !important;border:1px solid rgba(255,255,255,0.07) !important;border-radius:10px !important;padding:12px 14px !important;}[data-testid='stMetricLabel'] p{color:#64748b !important;font-size:0.72rem !important;font-family:'Space Mono',monospace !important;text-transform:uppercase;letter-spacing:1px;}[data-testid='stMetricValue']{color:#00d4ff !important;font-family:'Space Mono',monospace !important;font-size:1.4rem !important;}</style>", unsafe_allow_html=True)
st.markdown("<style>[data-testid='stChatInput']{border:1.5px solid #00d4ff !important;border-radius:14px !important;background:#0e1623 !important;padding:4px 8px !important;}[data-testid='stChatInput'] textarea{background:transparent !important;color:#e2e8f0 !important;font-family:'DM Sans',sans-serif !important;font-size:0.95rem !important;}[data-testid='stChatInput'] button{background:#00d4ff !important;border-radius:8px !important;color:#000 !important;}</style>", unsafe_allow_html=True)
st.markdown("<style>[data-testid='stSpinner'] p{color:#00d4ff !important;font-family:'Space Mono',monospace !important;font-size:0.8rem;}::-webkit-scrollbar{width:4px;height:4px;}::-webkit-scrollbar-track{background:#080c14;}::-webkit-scrollbar-thumb{background:#1e2d42;border-radius:2px;}</style>", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for key, val in [
    ("conversation_history", []),
    ("chat_display", []),
    ("tool_calls_count", 0),
    ("session_start", datetime.now().strftime("%H:%M")),
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── TOOL METADATA ─────────────────────────────────────────────────────────────
TOOLS_META = {
    "get_weather":        ("🌤️", "Weather",   "#00d4ff"),
    "convert_currency":   ("💱", "Currency",  "#10b981"),
    "get_news":           ("📰", "News",      "#f59e0b"),
    "analyze_sentiment":  ("😊", "Sentiment", "#7c3aed"),
    "add_expense":        ("➕", "Add Exp.",  "#ec4899"),
    "list_expenses":      ("📋", "List Exp.", "#ec4899"),
    "summarize_expenses": ("📊", "Summary",   "#ec4899"),
}

EXAMPLES = [
    ("🌤️", "What's the weather in Mumbai?"),
    ("💱", "Convert 500 USD to INR"),
    ("📰", "Latest news on artificial intelligence"),
    ("😊", "Analyze: This project is absolutely incredible!"),
    ("➕", "Add expense: 350 for food today"),
    ("📋", "Show my expenses this month"),
]

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="padding:16px 0 12px;border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:16px;"><div style="font-family:Space Mono,monospace;font-size:1rem;font-weight:700;color:#00d4ff;">⚡ MCP SYSTEM</div><div style="font-size:0.7rem;color:#64748b;margin-top:3px;">Model Context Protocol · v1.0</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.metric("Messages", len(st.session_state.chat_display))
    c2.metric("Tool Calls", st.session_state.tool_calls_count)

    st.markdown('<div style="font-family:Space Mono,monospace;font-size:0.62rem;color:#64748b;letter-spacing:2px;text-transform:uppercase;margin:16px 0 8px;">Registered Tools</div>', unsafe_allow_html=True)

    for icon, label, color in TOOLS_META.values():
        st.markdown(f'<div style="display:flex;align-items:center;gap:10px;padding:6px 10px;border-radius:7px;border:1px solid rgba(255,255,255,0.06);background:#0e1623;margin-bottom:4px;"><span>{icon}</span><span style="font-size:0.8rem;color:#cbd5e1;">{label}</span><span style="margin-left:auto;width:7px;height:7px;border-radius:50%;background:{color};box-shadow:0 0 6px {color};"></span></div>', unsafe_allow_html=True)

    st.markdown('<div style="font-family:Space Mono,monospace;font-size:0.62rem;color:#64748b;letter-spacing:2px;text-transform:uppercase;margin:16px 0 8px;">Quick Prompts</div>', unsafe_allow_html=True)

    for icon, example in EXAMPLES:
        if st.button(f"{icon}  {example}", key=example, use_container_width=True):
            st.session_state.pending_query = example

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if st.button("🗑️  Clear Chat", use_container_width=True):
        st.session_state.conversation_history = []
        st.session_state.chat_display = []
        st.session_state.tool_calls_count = 0
        st.rerun()

    st.markdown(f'<div style="margin-top:24px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.05);font-size:0.68rem;color:#334155;font-family:Space Mono,monospace;line-height:1.8;">Session · {st.session_state.session_start}<br>Samdeesh Singh · 102203005<br>Thapar Institute · HCL Tech</div>', unsafe_allow_html=True)

# ── MAIN AREA ─────────────────────────────────────────────────────────────────
if len(st.session_state.chat_display) == 0:
    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;padding:0 24px;"><div style="width:64px;height:64px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#00d4ff,#7c3aed);box-shadow:0 0 32px rgba(0,212,255,0.35);margin:0 auto 20px;font-size:1.8rem;display:flex;align-items:center;justify-content:center;">⚡</div><h1 style="font-family:Space Mono,monospace;font-size:1.8rem;font-weight:700;color:#e2e8f0;letter-spacing:-1px;margin:0 0 10px;">MCP Intelligent Tool System</h1><p style="color:#64748b;font-size:0.95rem;max-width:480px;margin:0 auto 28px;line-height:1.7;">Powered by <span style="color:#00d4ff;">Groq LLaMA 3</span> + <span style="color:#7c3aed;">Model Context Protocol</span>. Ask anything in plain English — the AI picks the right tool automatically.</p></div>', unsafe_allow_html=True)

    cols = st.columns(5)
    pills = [("🌤️","Weather","#00d4ff"),("💱","Currency","#10b981"),
             ("📰","News","#f59e0b"),("😊","Sentiment","#7c3aed"),("💰","Expenses","#ec4899")]
    for col, (icon, label, color) in zip(cols, pills):
        col.markdown(f'<div style="text-align:center;padding:10px 6px;border-radius:10px;border:1px solid {color}33;background:{color}08;"><div style="font-size:1.3rem;">{icon}</div><div style="font-size:0.72rem;color:{color};margin-top:4px;font-family:Space Mono,monospace;">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;font-family:Space Mono,monospace;font-size:0.68rem;color:#334155;letter-spacing:2px;text-transform:uppercase;">↓ type a message or pick a prompt from the sidebar</p>', unsafe_allow_html=True)

else:
    for msg in st.session_state.chat_display:
        if msg["role"] == "user":
            st.markdown(f'<div style="display:flex;justify-content:flex-end;margin:8px 0;"><div style="max-width:72%;background:linear-gradient(135deg,#1a3a54,#122840);border:1px solid #1e4a6a;border-radius:16px 16px 3px 16px;padding:11px 16px;font-size:0.92rem;color:#e2e8f0;line-height:1.55;box-shadow:0 2px 10px rgba(0,0,0,0.3);">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            tool_key   = msg.get("tool")
            badge_html = ""
            left_color = "#1e2d42"

            if tool_key and tool_key in TOOLS_META:
                icon, label, color = TOOLS_META[tool_key]
                left_color = color
                badge_html = f'<div style="display:flex;align-items:center;gap:5px;margin-bottom:7px;"><span style="font-size:0.8rem;">{icon}</span><span style="font-family:Space Mono,monospace;font-size:0.6rem;color:{color};letter-spacing:1.5px;text-transform:uppercase;">{label} tool</span></div>'

            clean = clean_response(msg["content"])
            st.markdown(f'<div style="display:flex;justify-content:flex-start;margin:8px 0;"><div style="max-width:82%;background:#0e1623;border:1px solid {left_color}33;border-left:3px solid {left_color};border-radius:3px 16px 16px 16px;padding:13px 17px;font-size:0.9rem;color:#cbd5e1;line-height:1.65;box-shadow:0 2px 14px rgba(0,0,0,0.25);"><div style="display:flex;align-items:center;gap:7px;margin-bottom:9px;"><div style="width:20px;height:20px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,#00d4ff,#7c3aed);display:flex;align-items:center;justify-content:center;font-size:0.6rem;">⚡</div><span style="font-family:Space Mono,monospace;font-size:0.62rem;color:#00d4ff;letter-spacing:1px;">MCP ASSISTANT</span></div>{badge_html}<div style="white-space:pre-wrap;">{clean}</div></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── CHAT INPUT ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask anything — weather, news, currency, sentiment, expenses...")

if "pending_query" in st.session_state:
    user_input = st.session_state.pending_query
    del st.session_state.pending_query

# ── PROCESS ───────────────────────────────────────────────────────────────────
if user_input:
    st.session_state.chat_display.append({"role": "user", "content": user_input})

    last_tool_used = {"name": None}
    import host.host as host_module
    original_execute = host_module.execute_tool

    def tracking_execute(tool_name, tool_input):
        last_tool_used["name"] = tool_name
        st.session_state.tool_calls_count += 1
        return original_execute(tool_name, tool_input)

    host_module.execute_tool = tracking_execute

    with st.spinner("⚡ Routing to the right tool..."):
        try:
            response = chat(user_input, st.session_state.conversation_history)
        except Exception as e:
            response = f"Something went wrong: {str(e)}"

    host_module.execute_tool = original_execute
    log_conversation(user_input, response, last_tool_used["name"])

    st.session_state.chat_display.append({
        "role": "assistant",
        "content": response,
        "tool": last_tool_used["name"]
    })

    st.rerun()