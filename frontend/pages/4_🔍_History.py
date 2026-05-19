

import streamlit as st
import sys, os, json
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from frontend.utils.logger import get_all_logs

st.set_page_config(page_title="History · MCP System", page_icon="🔍", layout="wide")

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">', unsafe_allow_html=True)
st.markdown("<style>html,body,[class*='css']{font-family:'DM Sans',sans-serif !important;background:#080c14 !important;color:#e2e8f0 !important;}#MainMenu,footer{visibility:hidden;}[data-testid='stAppViewContainer']{background:#080c14 !important;}[data-testid='stSidebar']{background:#0e1623 !important;border-right:1px solid rgba(255,255,255,0.07) !important;}.block-container{padding:2rem !important;}</style>", unsafe_allow_html=True)
st.markdown("<style>input{background:#0e1623 !important;color:#e2e8f0 !important;border:1px solid rgba(255,255,255,0.1) !important;border-radius:8px !important;}div[data-baseweb='select']>div{background:#0e1623 !important;border:1px solid rgba(255,255,255,0.1) !important;color:#e2e8f0 !important;}</style>", unsafe_allow_html=True)

st.markdown('<h1 style="font-family:Space Mono,monospace;font-size:1.6rem;color:#e2e8f0;margin-bottom:4px;">🔍 Query History</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#64748b;font-size:0.9rem;margin-bottom:24px;">Search and browse every conversation across all sessions</p>', unsafe_allow_html=True)

logs = get_all_logs()

if not logs:
    st.markdown('<div style="text-align:center;padding:60px;color:#334155;font-family:Space Mono,monospace;font-size:0.85rem;">No conversations logged yet.<br>Start chatting on the main page!</div>', unsafe_allow_html=True)
    st.stop()


col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search = st.text_input("🔎 Search by keyword", placeholder="e.g. weather, bitcoin, sentiment...")

with col2:
    all_tools = sorted(set(e.get("tool_used", "none") or "none" for e in logs))
    tool_filter = st.selectbox("Filter by tool", ["All tools"] + all_tools)

with col3:
    all_dates = sorted(set(e["timestamp"][:10] for e in logs), reverse=True)
    date_filter = st.selectbox("Filter by date", ["All dates"] + all_dates)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)


filtered = logs

if search:
    kw = search.lower()
    filtered = [e for e in filtered if kw in e["user"].lower() or kw in e["assistant"].lower()]

if tool_filter != "All tools":
    filtered = [e for e in filtered if (e.get("tool_used") or "none") == tool_filter]

if date_filter != "All dates":
    filtered = [e for e in filtered if e["timestamp"][:10] == date_filter]

filtered = list(reversed(filtered))


c1, c2, c3 = st.columns(3)
c1.metric("Total Conversations", len(logs))
c2.metric("Matching Results", len(filtered))
c3.metric("Unique Dates", len(all_dates))

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)


TOOL_COLORS = {
    "get_weather": "#00d4ff", "convert_currency": "#10b981",
    "get_news": "#f59e0b", "analyze_sentiment": "#7c3aed",
    "add_expense": "#ec4899", "list_expenses": "#ec4899",
    "summarize_expenses": "#ec4899", "none": "#64748b"
}

TOOL_ICONS = {
    "get_weather": "🌤️", "convert_currency": "💱",
    "get_news": "📰", "analyze_sentiment": "😊",
    "add_expense": "➕", "list_expenses": "📋",
    "summarize_expenses": "📊", "none": "💬"
}


if not filtered:
    st.markdown('<div style="text-align:center;padding:48px;color:#334155;font-family:Space Mono,monospace;">No results found for your filters.</div>', unsafe_allow_html=True)
else:
    for entry in filtered:
        tool   = entry.get("tool_used") or "none"
        color  = TOOL_COLORS.get(tool, "#64748b")
        icon   = TOOL_ICONS.get(tool, "💬")
        ts     = entry["timestamp"]
        user_q = entry["user"]
        ai_ans = entry["assistant"][:300] + ("..." if len(entry["assistant"]) > 300 else "")

      
        def highlight(text, kw):
            if not kw:
                return text
            import re
            return re.sub(f"(?i)({re.escape(kw)})",
                          r'<mark style="background:#00d4ff22;color:#00d4ff;border-radius:3px;padding:0 2px;">\1</mark>',
                          text)

        user_hl = highlight(user_q, search)
        ai_hl   = highlight(ai_ans, search)

        st.markdown(f"""
        <div style="background:#0e1623;border:1px solid {color}22;border-left:3px solid {color};
                    border-radius:4px 12px 12px 12px;padding:14px 18px;margin-bottom:10px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
            <div style="display:flex;align-items:center;gap:8px;">
              <span style="font-size:0.9rem;">{icon}</span>
              <span style="font-family:Space Mono,monospace;font-size:0.62rem;color:{color};
                           letter-spacing:1.5px;text-transform:uppercase;">{tool.replace("_"," ")}</span>
            </div>
            <span style="font-family:Space Mono,monospace;font-size:0.65rem;color:#475569;">{ts}</span>
          </div>
          <div style="margin-bottom:8px;">
            <span style="font-size:0.72rem;color:#64748b;font-family:Space Mono,monospace;
                         letter-spacing:1px;text-transform:uppercase;">You asked</span>
            <div style="font-size:0.9rem;color:#e2e8f0;margin-top:4px;padding:8px 10px;
                        background:#151f2e;border-radius:6px;">{user_hl}</div>
          </div>
          <div>
            <span style="font-size:0.72rem;color:#64748b;font-family:Space Mono,monospace;
                         letter-spacing:1px;text-transform:uppercase;">AI responded</span>
            <div style="font-size:0.88rem;color:#94a3b8;margin-top:4px;padding:8px 10px;
                        background:#0a1628;border-radius:6px;line-height:1.6;">{ai_hl}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
