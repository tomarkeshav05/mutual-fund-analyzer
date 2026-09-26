import sqlite3

# This creates a new database file called mutual_funds.db in your project folder
conn = sqlite3.connect("mutual_funds.db")
cursor = conn.cursor()

# Create the funds table
cursor.execute("""
CREATE TABLE IF NOT EXISTS funds (
    scheme_code INTEGER PRIMARY KEY,
    scheme_name TEXT,
    category TEXT,
    fund_house TEXT
)
""")

# Create the nav_history table
cursor.execute("""
CREATE TABLE IF NOT EXISTS nav_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER,
    nav_date DATE,
    nav_value FLOAT,
    FOREIGN KEY (scheme_code) REFERENCES funds(scheme_code)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS fund_metrics (
    scheme_code INTEGER PRIMARY KEY,
    category TEXT,
    scheme_name TEXT,
    years_of_data FLOAT,
    cagr FLOAT,
    volatility FLOAT,
    FOREIGN KEY (scheme_code) REFERENCES funds(scheme_code)
)
""")
# Add an is_active flag to funds table (safe to run even if column already exists)
try:
    cursor.execute("ALTER TABLE funds ADD COLUMN is_active INTEGER DEFAULT 1")
except sqlite3.OperationalError:
    pass  # column already exists, ignore
conn.commit()
conn.close()

print("Database and tables created successfully!")