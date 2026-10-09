# Mutual Fund Analyzer

An interactive web app that analyzes **252 mutual funds** using 12–13 years of historical data. It calculates **CAGR** and **volatility** for each fund and assigns a **4-level risk rating**, so you can compare returns against risk at a glance.

**Live app:** https://mutual-fund-analyzer1710.streamlit.app/

## Features

- Analysis of 252 mutual funds based on 12–13 years of historical NAV data
- **CAGR** (Compound Annual Growth Rate) to measure long-term returns
- **Volatility** to measure how much a fund's returns fluctuate
- **4-level risk rating** for each fund, based on historical returns and volatility
- Interactive interface for exploring and comparing funds

## How It Works

1. **Data collection:** historical NAV data is fetched from [MFAPI](https://www.mfapi.in/).
2. **Metric calculation:** CAGR and volatility are calculated for each fund from its past data.
3. **Risk rating:** each fund is placed into one of 4 risk levels using its calculated metrics.
4. **Visualization:** results are shown in an interactive Streamlit dashboard.

### Formulas

```
CAGR       = (Ending NAV / Starting NAV) ^ (1 / Years) - 1
Volatility = Standard deviation of periodic returns (annualized)
```

## Tech Stack

- Python
- Streamlit
- MFAPI (data source)
- <!-- Add other libraries you used, e.g. Pandas, NumPy, Plotly -->

## Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/tomarkeshav05/mutual-fund-analyzer.git
cd mutual-fund-analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
streamlit run app.py
```

<!-- If your main file is not app.py, replace it in the last command -->

## Project Structure

```
mutual-fund-analyzer/
├── app.py              # Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```
<!-- Update this to match your actual files -->

## Limitations

- Past performance does not guarantee future returns.
- The risk rating is based only on historical data and is meant for comparison, not as a complete risk assessment.

## Disclaimer

This project is for educational purposes only and is **not financial advice**. Consult a qualified financial advisor before making investment decisions.

## Author

**Keshav Tomar**
[LinkedIn](https://www.linkedin.com/in/keshav-tomar-46294a391) | [GitHub](https://github.com/tomarkeshav05)
