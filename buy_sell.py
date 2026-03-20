

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


print("Fetching Tesla data...")

stock = yf.Ticker("RELIANCE.NS")
data = stock.history(period="3mo")

print("✅ Data fetched!")

# ----- Step 2: Moving Averages Calculate Karo -----
# MA20 = Last 20 days ka average
# MA50 = Last 50 days ka average
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()

print("✅ Moving averages calculated!")

# ----- Step 3: Buy/Sell Signals Dhundho -----
buy_signals = []
sell_signals = []

for i in range(len(data)):
    if data['MA20'].iloc[i] > data['MA50'].iloc[i]:
        buy_signals.append(data['Close'].iloc[i])
        sell_signals.append(None)
    elif data['MA20'].iloc[i] < data['MA50'].iloc[i]:
        sell_signals.append(data['Close'].iloc[i])
        buy_signals.append(None)
    else:
        buy_signals.append(None)
        sell_signals.append(None)

data['Buy'] = buy_signals
data['Sell'] = sell_signals


print("\nCreating Buy/Sell Signal Chart...")

fig = go.Figure()

# Actual price line
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Close'],
    mode='lines',
    name='Tesla Price',
    line=dict(color='white', width=1.5)
))

# MA20 line
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['MA20'],
    mode='lines',
    name='MA20 (20 days avg)',
    line=dict(color='royalblue', width=1.5, dash='dash')
))

# MA50 line
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['MA50'],
    mode='lines',
    name='MA50 (50 days avg)',
    line=dict(color='orange', width=1.5, dash='dash')
))

# Buy signals
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Buy'],
    mode='markers',
    name='BUY Signal 🟢',
    marker=dict(color='lime', size=8, symbol='triangle-up')
))

# Sell signals
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Sell'],
    mode='markers',
    name='SELL Signal 🔴',
    marker=dict(color='red', size=8, symbol='triangle-down')
))

fig.update_layout(
    title="Tesla — Buy / Sell Signals",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    template="plotly_dark",
    hovermode="x unified"
)

fig.show()

print("✅ Signal Chart ready!")
