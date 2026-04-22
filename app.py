import streamlit as st
import pandas as pd

st.set_page_config(page_title="Interview Dashboard", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1e1e2f, #2c2c54);
    color: white;
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: white;
}
.card {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 20px;
    font-weight: bold;
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}
.l1 {background: linear-gradient(135deg, #f7971e, #ffd200);}
.l2 {background: linear-gradient(135deg, #36d1dc, #5b86e5);}
.l3 {background: linear-gradient(135deg, #a18cd1, #fbc2eb);}
.final {background: linear-gradient(135deg, #00b09b, #96c93d);}
.reject {background: linear-gradient(135deg, #ff416c, #ff4b2b);}
.section {
    font-size: 24px;
    font-weight: 600;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<div class='title'>📊 Interview Pipeline Dashboard</div>", unsafe_allow_html=True)
st.write("---")

# ---------------- LOAD DATA ----------------
sheet_id = "1vYu-xYB5T-_Sl-YL-_9pBcSnCQ_j3bDB5kPuq4Ey6Bc"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

df = pd.read_csv(url)
df["Stage"] = df["Stage"].astype(str).str.upper()
df["Status"] = df["Status"].astype(str).str.upper()

# ---------------- FILTER ----------------
client = st.selectbox("Filter by Client", ["All"] + list(df["Client"].dropna().unique()))
filtered_df = df if client == "All" else df[df["Client"] == client]

# ---------------- LOGIC ----------------

# Ongoing
l1_round_df = filtered_df[(filtered_df["Stage"].str.contains("L1")) & (~filtered_df["Stage"].str.contains("SELECT"))]
l2_round_df = filtered_df[(filtered_df["Stage"].str.contains("L2")) & (~filtered_df["Stage"].str.contains("SELECT"))]
l3_round_df = filtered_df[(filtered_df["Stage"].str.contains("L3")) & (~filtered_df["Stage"].str.contains("SELECT"))]

# Cleared
l1_select_df = filtered_df[filtered_df["Stage"].str.contains("L1 SELECT")]
l2_select_df = filtered_df[filtered_df["Stage"].str.contains("L2 SELECT")]
l3_select_df = filtered_df[filtered_df["Stage"].str.contains("L3 SELECT")]

# Final + Reject
final_df = filtered_df[filtered_df["Status"].str.contains("SELECT")]
reject_df = filtered_df[filtered_df["Status"].str.contains("REJECT")]

# Counts
l1_round = len(l1_round_df)
l2_round = len(l2_round_df)
l3_round = len(l3_round_df)

l1_select = len(l1_select_df)
l2_select = len(l2_select_df)
l3_select = len(l3_select_df)

final_count = len(final_df)
reject_count = len(reject_df)

# ---------------- CARDS ----------------

st.markdown("## 🔄 Ongoing Interviews")

col1, col2, col3 = st.columns(3)
col1.markdown(f"<div class='card l1'>🟡 L1 Round<br><h1>{l1_round}</h1></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='card l2'>🔵 L2 Round<br><h1>{l2_round}</h1></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='card l3'>🟣 L3 Round<br><h1>{l3_round}</h1></div>", unsafe_allow_html=True)

st.markdown("## ✅ Cleared Candidates")

col4, col5, col6 = st.columns(3)
col4.markdown(f"<div class='card l1'>🟡 L1 Select<br><h1>{l1_select}</h1></div>", unsafe_allow_html=True)
col5.markdown(f"<div class='card l2'>🔵 L2 Select<br><h1>{l2_select}</h1></div>", unsafe_allow_html=True)
col6.markdown(f"<div class='card l3'>🟣 L3 Select<br><h1>{l3_select}</h1></div>", unsafe_allow_html=True)

st.markdown("## 🎯 Final Outcome")

col7, col8 = st.columns(2)
col7.markdown(f"<div class='card final'>🟢 Final Selected<br><h1>{final_count}</h1></div>", unsafe_allow_html=True)
col8.markdown(f"<div class='card reject'>❌ Rejected<br><h1>{reject_count}</h1></div>", unsafe_allow_html=True)

st.write("---")

# ---------------- TABLES ----------------

st.markdown("## 🔄 Ongoing Interview Details")

st.markdown("### 🟡 L1 Round")
st.dataframe(l1_round_df, use_container_width=True, hide_index=True)

st.markdown("### 🔵 L2 Round")
st.dataframe(l2_round_df, use_container_width=True, hide_index=True)

st.markdown("### 🟣 L3 Round")
st.dataframe(l3_round_df, use_container_width=True, hide_index=True)

st.markdown("## ✅ Cleared Candidates Details")

st.markdown("### 🟡 L1 Select")
st.dataframe(l1_select_df, use_container_width=True, hide_index=True)

st.markdown("### 🔵 L2 Select")
st.dataframe(l2_select_df, use_container_width=True, hide_index=True)

st.markdown("### 🟣 L3 Select")
st.dataframe(l3_select_df, use_container_width=True, hide_index=True)

st.markdown("## 🎯 Final Outcome Details")

st.markdown("### 🟢 Final Select")
st.dataframe(final_df, use_container_width=True, hide_index=True)

st.markdown("### ❌ Reject")
st.dataframe(reject_df, use_container_width=True, hide_index=True)
