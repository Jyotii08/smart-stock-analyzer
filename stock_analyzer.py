
# Smart Stock Analyzer — by [Jyoti saw]
# Fetching & Understanding Stock Data


import yfinance as yf
import pandas as pd



stock_name = "TSLA"   # Tesla Industries

print(f"📈 Fetching data for: {stock_name}")
print("Please wait...")


# Last 3 months ka data laate hain
stock = yf.Ticker(stock_name)
data = stock.history(period="3mo")


print("\n========== Stock Data Summary ==========")
print(f"✅ Total trading days  : {len(data)}")
print(f"📅 From               : {data.index[0].date()}")
print(f"📅 To                 : {data.index[-1].date()}")
print(f"💰 Highest Price      : ₹{data['High'].max():.2f}")
print(f"💰 Lowest Price       : ₹{data['Low'].min():.2f}")
print(f"💰 Current Price      : ₹{data['Close'][-1]:.2f}")

data.to_csv("stock_data.csv")
print("\n📁 Data saved to stock_data.csv")
print("\n✅ Day 1 Complete — Stock data fetched successfully!")
# ----- Step 5: Basic Analysis -----
print("\n========== Basic Analysis ==========")

# Average price
avg_price = data['Close'].mean()
print(f"📊 Average Price (3 months) : ₹{avg_price:.2f}")

# Price change
first_price = data['Close'][0]
last_price = data['Close'][-1]
change = ((last_price - first_price) / first_price) * 100
print(f"📈 Price Change             : {change:.2f}%")

if change > 0:
    print("✅ Stock is UP in last 3 months!")
elif change < 0:
    print("❌ Stock is DOWN in last 3 months!")
else:
    print("➡️ Stock is STABLE!")

# Best & Worst day
best_day = data['Close'].idxmax()
worst_day = data['Close'].idxmin()
print(f"🏆 Best Day  : {best_day.date()} — ₹{data['Close'].max():.2f}")
print(f"📉 Worst Day : {worst_day.date()} — ₹{data['Close'].min():.2f}")

print("\n✅ Basic Analysis Complete!")