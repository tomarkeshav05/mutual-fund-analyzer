import sqlite3
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

conn = sqlite3.connect("mutual_funds.db")

# Load fund metrics into a pandas DataFrame (much easier to work with for ML)
df = pd.read_sql_query("""
    SELECT fm.* FROM fund_metrics fm
    JOIN funds f ON fm.scheme_code = f.scheme_code
    WHERE f.is_active = 1
""", conn)

print("Loaded data:")
print(df[['scheme_name', 'category', 'cagr', 'volatility']])
print(f"\nTotal funds: {len(df)}")

# Drop any rows with missing CAGR or volatility (can't cluster incomplete data)
df_clean = df.dropna(subset=['cagr', 'volatility'])
print(f"Funds after removing incomplete rows: {len(df_clean)}")

conn.close()

# Select the features we want to cluster on
features = df_clean[['cagr', 'volatility']]

# Standardize the features (important! CAGR and volatility are on different scales)
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Run K-Means with 4 clusters (we'll try 4 risk-return "profiles")
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_clean = df_clean.copy()
df_clean['cluster'] = kmeans.fit_predict(features_scaled)

# Show results grouped by cluster
print("\n=== FUNDS GROUPED BY CLUSTER ===\n")
for cluster_num in sorted(df_clean['cluster'].unique()):
    cluster_funds = df_clean[df_clean['cluster'] == cluster_num]
    avg_cagr = cluster_funds['cagr'].mean()
    avg_vol = cluster_funds['volatility'].mean()
    print(f"--- Cluster {cluster_num} (avg CAGR: {avg_cagr:.2f}%, avg Volatility: {avg_vol:.2f}%) ---")
    for _, row in cluster_funds.iterrows():
        print(f"  {row['category']:12} | CAGR: {row['cagr']:6.2f}% | Vol: {row['volatility']:6.2f}% | {row['scheme_name']}")
    print()