import streamlit as st
import sqlite3
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px

st.set_page_config(page_title="Mutual Fund Risk-Return Analyzer", layout="wide", page_icon="📊")

# ---------- CUSTOM STYLING ----------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    .stApp {
        background-color: #0A2E28;
        font-family: 'Inter', sans-serif;
    }
    h1 {
        font-family: 'Playfair Display', serif !important;
        color: #F0EAE0 !important;
        font-weight: 700 !important;
        font-size: 2.8rem !important;
    }
    h2, h3 {
        font-family: 'Inter', sans-serif !important;
        color: #F0EAE0 !important;
        font-weight: 600 !important;
        border-left: 3px solid #C9A24B;
        padding-left: 12px;
    }
    p, li, span, label {
        color: #D8D0C0 !important;
    }
    div[data-testid="stMetric"] {
        background: #0F3A32;
        border-radius: 4px;
        padding: 16px 20px;
        border: none;
        border-bottom: 2px solid #C9A24B;
    }
    div[data-testid="stMetricValue"] {
        color: #C9A24B !important;
        font-family: 'Playfair Display', serif !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #A8A296 !important;
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #0F3A32 !important;
        color: #F0EAE0 !important;
        border: 1px solid #2A5A4E !important;
        border-radius: 4px !important;
    }
    .stDataFrame {
        border: 1px solid #2A5A4E;
        border-radius: 4px;
    }
    div[data-testid="stRadio"] label {
        color: #F0EAE0 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Mutual Fund Risk-Return Analyzer")
st.write("Explore 200+ mutual funds by risk and return profile, clustered using machine learning.")


# ---------- DATA LOADING ----------
@st.cache_data
def load_data():
    conn = sqlite3.connect("mutual_funds.db")
    df = pd.read_sql_query("""
        SELECT fm.* FROM fund_metrics fm
        JOIN funds f ON fm.scheme_code = f.scheme_code
        WHERE f.is_active = 1
    """, conn)
    conn.close()
    return df

df = load_data()

# ---------- CLUSTERING ----------
features = df[['cagr', 'volatility']]
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(features_scaled)

cluster_stats = df.groupby('cluster').agg(avg_vol=('volatility', 'mean'), avg_cagr=('cagr', 'mean'))
cluster_stats = cluster_stats.sort_values('avg_vol')

risk_labels = ['Conservative', 'Moderate', 'Growth-Oriented', 'Aggressive']
cluster_to_label = {}
for i, (cluster_id, row) in enumerate(cluster_stats.iterrows()):
    base_label = risk_labels[i]
    # Flag clusters where risk isn't being rewarded with return
    if row['avg_cagr'] < 3:
        base_label += " (Weak Returns)"
    cluster_to_label[cluster_id] = base_label

df['risk_profile'] = df['cluster'].map(cluster_to_label)

# For the radio button, use the actual labels present in the data (may include flagged ones)
available_risk_profiles = df['risk_profile'].unique().tolist()
# Sort them to roughly match risk_labels order for consistent display
def sort_key(label):
    for i, base in enumerate(risk_labels):
        if label.startswith(base):
            return i
    return 99
available_risk_profiles.sort(key=sort_key)

# ---------- CHART ----------
st.header("📈 All Funds: Risk vs Return")

fig = px.scatter(
    df, x='volatility', y='cagr', color='risk_profile',
    hover_data=['scheme_name', 'category'],
    labels={'volatility': 'Volatility (Risk) %', 'cagr': 'CAGR (Return) %'},
    color_discrete_map={
    'Conservative': '#C9A24B',
    'Moderate': '#6B9080',
    'Growth-Oriented': '#D9785D',
    'Aggressive': '#A63A50',
    'Aggressive (Weak Returns)': '#7A3B4A',
    'Moderate (Weak Returns)': '#8A8378',
    'Conservative (Weak Returns)': '#9C8A5E',
    'Growth-Oriented (Weak Returns)': '#B85C42'
}
    
)
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='#F0EAE0',
    font_family='Inter'
)
st.plotly_chart(fig, use_container_width=True)

# ---------- SEARCH + DROPDOWN ----------
st.header("🔍 Look up a specific fund")

search_term = st.text_input("Search by fund name or category:", "")

if search_term:
    filtered_df = df[
        df['scheme_name'].str.contains(search_term, case=False) |
        df['category'].str.contains(search_term, case=False)
    ]
else:
    filtered_df = df

if len(filtered_df) == 0:
    st.warning("No funds match your search. Try a different term.")
else:
    fund_names = filtered_df['scheme_name'].tolist()
    selected_fund = st.selectbox(f"Choose a fund ({len(fund_names)} matches):", fund_names)

    fund_row = df[df['scheme_name'] == selected_fund].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CAGR", f"{fund_row['cagr']:.2f}%")
    col2.metric("Volatility", f"{fund_row['volatility']:.2f}%")
    col3.metric("Category", fund_row['category'])
    col4.metric("Risk Profile", fund_row['risk_profile'])

    st.subheader("Similar funds (same cluster)")
    similar_funds = df[(df['cluster'] == fund_row['cluster']) & (df['scheme_name'] != selected_fund)]
    st.dataframe(
        similar_funds[['scheme_name', 'category', 'cagr', 'volatility']].reset_index(drop=True),
        use_container_width=True
    )

# ---------- RISK APPETITE RECOMMENDER ----------
st.header("🎯 Get recommendations based on your risk appetite")

risk_choice = st.radio("What's your risk appetite?", available_risk_profiles, horizontal=True)
recommended = df[df['risk_profile'] == risk_choice].sort_values('cagr', ascending=False)

st.write(f"Showing {len(recommended)} funds matching **{risk_choice}** risk profile:")
st.dataframe(
    recommended[['scheme_name', 'category', 'cagr', 'volatility']].reset_index(drop=True),
    use_container_width=True
)
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px 0; color: #A8A296; font-size: 0.9rem;'>
    Built by <strong style='color: #C9A24B;'>[Keshav Tomar ]</strong> · Data from mfapi.in · 
    <a href="https://www.linkedin.com/in/[keshav-tomar-46294a391]" style='color: #C9A24B;'>LinkedIn</a> · 
    <a href="https://github.com/tomarkeshav05/mutual-fund-analyzer" style='color: #C9A24B;'>GitHub</a>
</div>
""", unsafe_allow_html=True)