import streamlit as st
import pandas as pd

st.set_page_config(page_title="Interview Dashboard", layout="wide")

# ---------------- STYLE (Premium Look) ----------------
st.markdown("""
<style>

/* Main App Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1e1e2f, #2c2c54);
    color: white;
}

/* Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #ffffff;
}

/* Cards */
.card {
    padding: 25px;
    border-radius: 16px;
    text-align: center;
    color: white;
    font-size: 22px;
    font-weight: bold;
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

/* Card colors */
.l1 {background: linear-gradient(135deg, #f7971e, #ffd200);}
.l2 {background: linear-gradient(135deg, #36d1dc, #5b86e5);}
.l3 {background: linear-gradient(135deg, #a18cd1, #fbc2eb);}
.final {background: linear-gradient(135deg, #11998e, #38ef7d);}

/* Section text */
.section {
    font-size: 24px;
    font-weight: 600;
    margin-top: 20px;
    color: #f1f1f1;
}

/* Table styling */
[data-testid="stDataFrame"] {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='title'>📊 Interview Pipeline Dashboard</div>", unsafe_allow_html=True)
st.write("")

# ---------------- LOAD DATA ----------------
sheet_id = "1vYu-xYB5T-_Sl-YL-_9pBcSnCQ_j3bDB5kPuq4Ey6Bc"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

df = pd.read_csv(url)

# Clean stage
df["Stage"] = df["Stage"].astype(str).str.upper()

# ---------------- COUNTS ----------------
l1 = len(df[df["Stage"].str.contains("L1", na=False)])
l2 = len(df[df["Stage"].str.contains("L2", na=False)])
l3 = len(df[df["Stage"].str.contains("L3", na=False)])
final = len(df[df["Stage"].str.contains("FINAL", na=False)])

# ---------------- CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='card l1'>🟡 L1<br><h1>{l1}</h1></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='card l2'>🔵 L2<br><h1>{l2}</h1></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='card l3'>🟣 L3<br><h1>{l3}</h1></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='card final'>🟢 Final<br><h1>{final}</h1></div>", unsafe_allow_html=True)

st.write("---")

# ---------------- FILTER ----------------
client = st.selectbox("Filter by Client", ["All"] + list(df["Client"].dropna().unique()))
filtered_df = df if client == "All" else df[df["Client"] == client]

l1_df = filtered_df[filtered_df["Stage"].str.contains("L1", na=False)]
l2_df = filtered_df[filtered_df["Stage"].str.contains("L2", na=False)]
l3_df = filtered_df[filtered_df["Stage"].str.contains("L3", na=False)]
final_df = filtered_df[filtered_df["Stage"].str.contains("FINAL", na=False)]

# ---------------- TABLES ----------------

st.markdown("<div class='section'>🟡 L1 Candidates</div>", unsafe_allow_html=True)
st.dataframe(l1_df, use_container_width=True, hide_index=True)

st.markdown("<div class='section'>🔵 L2 Candidates</div>", unsafe_allow_html=True)
st.dataframe(l2_df, use_container_width=True, hide_index=True)

st.markdown("<div class='section'>🟣 L3 Candidates</div>", unsafe_allow_html=True)
st.dataframe(l3_df, use_container_width=True, hide_index=True)

st.markdown("<div class='section'>🟢 Final Candidates</div>", unsafe_allow_html=True)
st.dataframe(final_df, use_container_width=True, hide_index=True)
