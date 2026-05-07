# frontend/pages/2_💰_Expenses.py

import streamlit as st
import sys, os, sqlite3
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

st.set_page_config(page_title="Expenses · MCP System", page_icon="💰", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] { font-family:'DM Sans',sans-serif !important; background:#080c14 !important; color:#e2e8f0 !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stAppViewContainer"] { background:#080c14 !important; }
[data-testid="stSidebar"] { background:#0e1623 !important; border-right:1px solid #1e2d42 !important; }
.block-container { padding:2rem !important; }
[data-testid="stMetric"] { background:#0e1623 !important; border:1px solid #1e2d42 !important; border-radius:10px !important; padding:16px !important; }
[data-testid="stMetricValue"] { color:#10b981 !important; font-family:'Space Mono',monospace !important; }
[data-testid="stMetricLabel"] { color:#64748b !important; font-size:0.75rem !important; }
input, select, textarea { background:#0e1623 !important; color:#e2e8f0 !important; border:1px solid #1e2d42 !important; border-radius:8px !important; }
.stButton button { background:#0e1623 !important; border:1px solid #1e2d42 !important; color:#e2e8f0 !important; border-radius:8px !important; }
.stButton button:hover { border-color:#10b981 !important; color:#10b981 !important; }
div[data-testid="stDataFrame"] { border:1px solid #1e2d42 !important; border-radius:10px !important; }
</style>
""", unsafe_allow_html=True)

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "server", "expenses.db"
)

def load_expenses():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            "SELECT * FROM expenses ORDER BY date DESC", conn
        )

def add_expense_direct(date, amount, category, note=""):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO expenses(date,amount,category,note) VALUES(?,?,?,?)",
            (date, amount, category, note)
        )

st.markdown("""
<h1 style="font-family:'Space Mono',monospace;font-size:1.6rem;color:#e2e8f0;margin-bottom:4px;">
  💰 Expense Manager
</h1>
<p style="color:#64748b;font-size:0.9rem;margin-bottom:28px;">
  View, add, and analyse your tracked expenses
</p>
""", unsafe_allow_html=True)

df = load_expenses()

# ── Metrics ──
if not df.empty:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Entries",    len(df))
    c2.metric("Total Spent",      f"₹ {df['amount'].sum():,.0f}")
    c3.metric("Average Expense",  f"₹ {df['amount'].mean():,.0f}")
    c4.metric("Top Category",     df.groupby("category")["amount"].sum().idxmax())

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Charts ──
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown("""<div style="font-family:'Space Mono',monospace;font-size:0.68rem;
                    color:#64748b;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">
                    Spending by Category</div>""", unsafe_allow_html=True)
        cat_df = df.groupby("category")["amount"].sum().reset_index()
        cat_df.columns = ["Category", "Amount (₹)"]
        st.bar_chart(cat_df.set_index("Category"), color="#10b981")

    with col_right:
        st.markdown("""<div style="font-family:'Space Mono',monospace;font-size:0.68rem;
                    color:#64748b;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">
                    Daily Spending Trend</div>""", unsafe_allow_html=True)
        trend_df = df.groupby("date")["amount"].sum().reset_index()
        trend_df.columns = ["Date", "Amount (₹)"]
        st.line_chart(trend_df.set_index("Date"), color="#ec4899")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Full table ──
    st.markdown("""<div style="font-family:'Space Mono',monospace;font-size:0.68rem;
                color:#64748b;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">
                All Transactions</div>""", unsafe_allow_html=True)
    st.dataframe(
        df[["date","category","amount","note"]].rename(columns={
            "date":"Date","category":"Category",
            "amount":"Amount (₹)","note":"Note"
        }),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No expenses yet. Add one below or use the chat!")

# ── Add expense form ──
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
st.markdown("""<div style="font-family:'Space Mono',monospace;font-size:0.68rem;
            color:#64748b;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;">
            Add New Expense</div>""", unsafe_allow_html=True)

with st.form("add_expense_form"):
    col1, col2, col3, col4 = st.columns([1.2, 1, 1.2, 1.5])
    with col1:
        date = st.date_input("Date")
    with col2:
        amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
    with col3:
        category = st.selectbox("Category", [
            "Food", "Transport", "Shopping", "Entertainment",
            "Health", "Education", "Utilities", "Other"
        ])
    with col4:
        note = st.text_input("Note (optional)")

    submitted = st.form_submit_button("➕  Add Expense", use_container_width=True)
    if submitted and amount > 0:
        add_expense_direct(str(date), amount, category, note)
        st.success(f"✅ Added ₹{amount} for {category}")
        st.rerun()