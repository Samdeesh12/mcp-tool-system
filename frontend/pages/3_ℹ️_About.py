# frontend/pages/3_ℹ️_About.py

import streamlit as st

st.set_page_config(page_title="About · MCP System", page_icon="ℹ️", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] { font-family:'DM Sans',sans-serif !important; background:#080c14 !important; color:#e2e8f0 !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stAppViewContainer"] { background:#080c14 !important; }
[data-testid="stSidebar"] { background:#0e1623 !important; border-right:1px solid #1e2d42 !important; }
.block-container { padding:2rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style="font-family:'Space Mono',monospace;font-size:1.6rem;color:#e2e8f0;margin-bottom:4px;">
  ℹ️ About This Project
</h1>
<p style="color:#64748b;font-size:0.9rem;margin-bottom:32px;">
  Design and Implementation of MCP-based Intelligent Tool Integration System
</p>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1.6, 1])

with col_left:
    st.markdown("""
    <div style="background:#0e1623;border:1px solid #1e2d42;border-radius:12px;padding:24px;margin-bottom:16px;">
      <div style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#00d4ff;
                  letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;">Project Overview</div>
      <p style="color:#94a3b8;font-size:0.9rem;line-height:1.8;">
        This project implements the <strong style="color:#e2e8f0;">Model Context Protocol (MCP)</strong> —
        an emerging standard for connecting AI systems to external tools and services.
        The system allows a Large Language Model to <em>dynamically discover</em> and invoke
        real-world tools based purely on natural language user queries.
      </p>
      <p style="color:#94a3b8;font-size:0.9rem;line-height:1.8;margin-top:12px;">
        Unlike vendor-specific solutions like LangChain or OpenAI function-calling,
        MCP provides a <strong style="color:#e2e8f0;">universal, reusable standard</strong>
        that can be extended across any business domain — making it highly relevant
        for enterprise environments like HCL Technologies.
      </p>
    </div>

    <div style="background:#0e1623;border:1px solid #1e2d42;border-radius:12px;padding:24px;margin-bottom:16px;">
      <div style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#10b981;
                  letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;">System Architecture</div>
      <div style="font-size:0.88rem;color:#94a3b8;line-height:2;">
        <div>🖥️ <strong style="color:#e2e8f0;">Presentation Layer</strong> — Streamlit multi-page web app</div>
        <div>🧠 <strong style="color:#e2e8f0;">Intelligence Layer</strong> — Groq LLaMA 3 via MCP Host</div>
        <div>⚙️ <strong style="color:#e2e8f0;">Tool Layer</strong> — MCP Server with 7 registered tools</div>
        <div>🌐 <strong style="color:#e2e8f0;">Data Layer</strong> — SQLite + 4 external REST APIs</div>
        <div>📡 <strong style="color:#e2e8f0;">Transport Layer</strong> — stdio (local) + HTTP SSE (remote)</div>
      </div>
    </div>

    <div style="background:#0e1623;border:1px solid #1e2d42;border-radius:12px;padding:24px;">
      <div style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#f59e0b;
                  letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;">Integrated APIs</div>
      <div style="display:flex;flex-wrap:wrap;gap:8px;">
        <span style="padding:5px 12px;border-radius:20px;background:rgba(0,212,255,0.07);
                     border:1px solid #1e3a4a;color:#00d4ff;font-size:0.8rem;">OpenWeatherMap API</span>
        <span style="padding:5px 12px;border-radius:20px;background:rgba(16,185,129,0.07);
                     border:1px solid #1e3a2e;color:#10b981;font-size:0.8rem;">ExchangeRate API</span>
        <span style="padding:5px 12px;border-radius:20px;background:rgba(245,158,11,0.07);
                     border:1px solid #3a2e1e;color:#f59e0b;font-size:0.8rem;">NewsAPI</span>
        <span style="padding:5px 12px;border-radius:20px;background:rgba(124,58,237,0.07);
                     border:1px solid #2e1e3a;color:#7c3aed;font-size:0.8rem;">HuggingFace Transformers</span>
        <span style="padding:5px 12px;border-radius:20px;background:rgba(236,72,153,0.07);
                     border:1px solid #3a1e2e;color:#ec4899;font-size:0.8rem;">Groq LLaMA 3</span>
        <span style="padding:5px 12px;border-radius:20px;background:rgba(99,102,241,0.07);
                     border:1px solid #1e1e3a;color:#818cf8;font-size:0.8rem;">SQLite</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div style="background:#0e1623;border:1px solid #1e2d42;border-radius:12px;padding:24px;margin-bottom:16px;">
      <div style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#7c3aed;
                  letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;">Student Details</div>
      <div style="font-size:0.88rem;color:#94a3b8;line-height:2.2;">
        <div>👤 <strong style="color:#e2e8f0;">Samdeesh Singh</strong></div>
        <div>🎓 Roll No. <strong style="color:#e2e8f0;">102203005</strong></div>
        <div>🏛️ <strong style="color:#e2e8f0;">Thapar Institute</strong></div>
        <div>🏢 Industry: <strong style="color:#e2e8f0;">HCL Technologies</strong></div>
        <div>👩‍🏫 Faculty: <strong style="color:#e2e8f0;">Miss Shivani Goswami</strong></div>
        <div>👨‍💼 Mentor: <strong style="color:#e2e8f0;">Mr Sachin Sharma</strong></div>
      </div>
    </div>

    <div style="background:#0e1623;border:1px solid #1e2d42;border-radius:12px;padding:24px;margin-bottom:16px;">
      <div style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#ec4899;
                  letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;">Tech Stack</div>
      <div style="font-size:0.85rem;color:#94a3b8;line-height:2.1;">
        <div>🐍 Python 3.13</div>
        <div>⚡ MCP SDK (FastMCP)</div>
        <div>🤖 Groq AI (LLaMA 3 70B)</div>
        <div>🤗 HuggingFace Transformers</div>
        <div>🎨 Streamlit</div>
        <div>🗄️ SQLite</div>
        <div>🔧 Git + GitHub</div>
      </div>
    </div>

    <div style="background:#0e1623;border:1px solid #1e2d42;border-radius:12px;padding:24px;">
      <div style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#00d4ff;
                  letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;">Timeline</div>
      <div style="font-size:0.83rem;color:#94a3b8;line-height:2.1;">
        <div>📚 <strong style="color:#64748b;">Month 1–1.5</strong> — Concepts & Research</div>
        <div>⚙️ <strong style="color:#64748b;">Month 1.5–2.5</strong> — MCP Server + Tools</div>
        <div>🧠 <strong style="color:#64748b;">Month 2.5–3.5</strong> — AI Integration</div>
        <div>🎨 <strong style="color:#64748b;">Month 3.5–4</strong> — Frontend + Testing</div>
        <div>📝 <strong style="color:#64748b;">Month 4–4.5</strong> — Docs + Submission</div>
      </div>
    </div>
    """, unsafe_allow_html=True)