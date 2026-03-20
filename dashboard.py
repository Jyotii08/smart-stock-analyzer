
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(
    page_title="Smart Stock Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Smart Stock Analyzer")
st.markdown("### Analyze any stock in real time!")
st.divider()

st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("Choose your stock and time period")

# Stock input
stock_input = st.sidebar.text_input(
    "Enter Stock Symbol",
    value="TSLA",
    help="Indian stocks: RELIANCE.NS | US stocks: TSLA, AAPL"
)

# Time period
period = st.sidebar.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y"],
    index=1,
    format_func=lambda x: {
        "1mo": "1 Month",
        "3mo": "3 Months",
        "6mo": "6 Months",
        "1y": "1 Year"
    }[x]
)

# Analyze button
analyze = st.sidebar.button("🔍 Analyze!", use_container_width=True)

if analyze or stock_input:
    
    # Data fetch karo
    with st.spinner(f"Fetching data for {stock_input}..."):
        stock = yf.Ticker(stock_input)
        data = stock.history(period=period)
        info = stock.info

    if len(data) == 0:
        st.error("❌ Stock not found! Please check the symbol.")
    
    else:
        # Company name
        company_name = info.get('longName', stock_input)
        st.subheader(f"🏢 {company_name}")

    
        col1, col2, col3, col4 = st.columns(4)

        current_price = data['Close'].iloc[-1]
        first_price = data['Close'].iloc[0]
        change = ((current_price - first_price) / first_price) * 100
        high = data['High'].max()
        low = data['Low'].min()

        col1.metric(
            "💰 Current Price",
            f"${current_price:.2f}",
            f"{change:.2f}%"
        )
        col2.metric("🔝 Period High", f"${high:.2f}")
        col3.metric("🔻 Period Low", f"${low:.2f}")
        col4.metric("📊 Total Trading Days", len(data))

        st.divider()

        st.subheader("📈 Price Trend")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name='Price',
            line=dict(color='royalblue', width=2)
        ))
        fig.update_layout(
            template="plotly_dark",
            hovermode="x unified",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

       
        st.subheader("🕯️ Candlestick Chart")

        candle = go.Figure()
        candle.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="OHLC"
        ))
        candle.update_layout(
            template="plotly_dark",
            hovermode="x unified",
            height=400
        )
        st.plotly_chart(candle, use_container_width=True)

        st.subheader("🔔 Buy / Sell Signals")

        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['MA50'] = data['Close'].rolling(window=50).mean()

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

        signal_fig = go.Figure()

        signal_fig.add_trace(go.Scatter(
            x=data.index, y=data['Close'],
            mode='lines', name='Price',
            line=dict(color='white', width=1.5)
        ))
        signal_fig.add_trace(go.Scatter(
            x=data.index, y=data['MA20'],
            mode='lines', name='MA20',
            line=dict(color='royalblue', dash='dash')
        ))
        signal_fig.add_trace(go.Scatter(
            x=data.index, y=data['MA50'],
            mode='lines', name='MA50',
            line=dict(color='orange', dash='dash')
        ))
        signal_fig.add_trace(go.Scatter(
            x=data.index, y=data['Buy'],
            mode='markers', name='BUY 🟢',
            marker=dict(color='lime', size=10, symbol='triangle-up')
        ))
        signal_fig.add_trace(go.Scatter(
            x=data.index, y=data['Sell'],
            mode='markers', name='SELL 🔴',
            marker=dict(color='red', size=10, symbol='triangle-down')
        ))

        signal_fig.update_layout(
            template="plotly_dark",
            hovermode="x unified",
            height=400
        )
        st.plotly_chart(signal_fig, use_container_width=True)

        st.subheader("📋 Raw Data")
        st.dataframe(data[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10))

        st.success("✅ Analysis Complete!")

st.divider()
st.markdown("Built with ❤️ by [Jyoti saw] | Data Source: Yahoo Finance")