# ============================================
# Smart Stock Analyzer — by [Tera Naam Yahan]
# Day 2 : Comparing Multiple Stocks
# ============================================

import yfinance as yf
import plotly.graph_objects as go

# ----- Step 1: Multiple Stocks Data Fetch Karo -----
print("Fetching data for multiple stocks...")

stocks = {
    "Tesla": "TSLA",
    "Apple": "AAPL",
    "Google": "GOOGL"
}

# ----- Step 2: Comparison Chart Banao -----
comparison_chart = go.Figure()

for name, symbol in stocks.items():
    stock = yf.Ticker(symbol)
    data = stock.history(period="3mo")
    
    print(f"✅ {name} data fetched!")
    
    comparison_chart.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name=name,
        hovertemplate=f"{name}<br>Date: %{{x}}<br>Price: $%{{y:.2f}}<extra></extra>"
    ))

comparison_chart.update_layout(
    title="Tesla vs Apple vs Google — Last 3 Months",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    template="plotly_dark",
    hovermode="x unified",
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )
)

comparison_chart.show()
print("\n✅ Comparison Chart ready!")