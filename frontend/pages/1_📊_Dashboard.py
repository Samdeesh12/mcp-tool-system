# frontend/pages/1_📊_Dashboard.py

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontend.utils.logger import get_all_logs, get_tool_usage_stats

st.set_page_config(page_title="Dashboard · MCP System", page_icon="📊", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; background: #080c14 !important; color: #e2e8f0 !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stAppViewContainer"] { background: #080c14 !important; }
[data-testid="stSidebar"] { background: #0e1623 !important; border-right: 1px solid #1e2d42 !important; }
[data-testid="stMetric"] { background: #0e1623 !important; border: 1px solid #1e2d42 !important; border-radius: 10px !important; padding: 16px !important; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #00d4ff !important; font-family: 'Space Mono', monospace !important; }
.block-container { padding: 2rem 2rem 2rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style="font-family:'Space Mono',monospace; font-size:1.6rem; color:#e2e8f0; margin-bottom:4px;">
  📊 Analytics Dashboard
</h1>
<p style="color:#64748b; font-size:0.9rem; margin-bottom:28px;">
  Live usage statistics across all sessions
</p>
""", unsafe_allow_html=True)

# ── Load data ──
logs = get_all_logs()
stats = get_tool_usage_stats()

# ── Top metrics ──
total_queries   = len(logs)
total_tool_calls = sum(stats.values())
top_tool = max(stats, key=stats.get) if stats else "None"
unique_days = len(set(e["timestamp"][:10] for e in logs)) if logs else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Queries",    total_queries)
c2.metric("Tool Calls Made",  total_tool_calls)
c3.metric("Most Used Tool",   top_tool.replace("_", " ").title() if top_tool != "None" else "None")
c4.metric("Active Days",      unique_days)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── Tool usage chart ──
if stats:
    import pandas as pd
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.72rem; color:#64748b;
                letter-spacing:2px; text-transform:uppercase; margin-bottom:12px;">
      Tool Usage Breakdown
    </div>
    """, unsafe_allow_html=True)

    df = pd.DataFrame(
        list(stats.items()),
        columns=["Tool", "Times Used"]
    ).sort_values("Times Used", ascending=False)

    df["Tool"] = df["Tool"].str.replace("_", " ").str.title()

    st.bar_chart(df.set_index("Tool"), color="#00d4ff")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── Recent conversations ──
st.markdown("""
<div style="font-family:'Space Mono',monospace; font-size:0.72rem; color:#64748b;
            letter-spacing:2px; text-transform:uppercase; margin-bottom:12px;">
  Recent Conversations
</div>
""", unsafe_allow_html=True)

if logs:
    for entry in reversed(logs[-10:]):
        tool_label = f"🔧 `{entry.get('tool_used', 'unknown')}`" if entry.get('tool_used') else ""
        st.markdown(f"""
        <div style="background:#0e1623; border:1px solid #1e2d42; border-radius:10px;
                    padding:12px 16px; margin-bottom:8px;">
          <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <span style="font-size:0.72rem; color:#64748b; font-family:'Space Mono',monospace;">
              {entry['timestamp']}
            </span>
            <span style="font-size:0.72rem; color:#00d4ff;">{tool_label}</span>
          </div>
          <div style="font-size:0.85rem; color:#94a3b8; margin-bottom:4px;">
            👤 {entry['user'][:120]}{'...' if len(entry['user']) > 120 else ''}
          </div>
          <div style="font-size:0.85rem; color:#475569;">
            ⚡ {entry['assistant'][:120]}{'...' if len(entry['assistant']) > 120 else ''}
          </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center; padding:48px; color:#334155;
                font-family:'Space Mono',monospace; font-size:0.8rem;">
      No conversations logged yet. Start chatting on the main page!
    </div>
    """, unsafe_allow_html=True)