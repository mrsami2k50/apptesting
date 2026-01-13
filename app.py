import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # suppress TensorFlow logs
os.environ['MPLBACKEND'] = 'Agg'         # ensure headless matplotlib

import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import warnings
import streamlit as st
from matplotlib.figure import Figure

# Streamlit header
# st.header("Stock Price Prediction: Lungteh Shipbuilding")
# Ignore warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

st.set_page_config(page_title="Stock Price Prediction", layout="wide")

# Stock info
# stock_no = '5234.TW'
# company_name = "Lungteh Shipbuilding"
stock_no = st.sidebar.text_input("Enter Stock Symbol (e.g., 5234.TW)", value="5234.TW")
company_name = st.sidebar.text_input("Enter Company Name", value="Lungteh Shipbuilding")

# st.set_page_config(
#     page_title=f"Stock Price Prediction for {company_name}",
#     layout="wide",      # <- This makes the page full-width
#     initial_sidebar_state="expanded"
# )

st.header(f"Stock Price Prediction: {company_name}")

# Date range
start_date = '2025-01-01'
end_date = '2026-05-30'

# Download historical stock data
df = yf.download(stock_no, start=start_date, end=end_date)
df = df.reset_index()
df.columns = df.columns.get_level_values(0)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)

# Prepare closing prices
close_prices = df['Close'].values.reshape(-1,1)

# Normalize
scaler = MinMaxScaler(feature_range=(0,1))
close_scaled = scaler.fit_transform(close_prices)

# Create sequences
sequence_length = 60
def create_dataset(data, seq_length):
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i-seq_length:i,0])
        y.append(data[i,0])
    return np.array(X), np.array(y)

X, y = create_dataset(close_scaled, sequence_length)
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1],1)))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train model
model.fit(X, y, epochs=20, batch_size=32, verbose=0)

# Predict next 7 days
last_60_days = close_scaled[-60:]
input_seq = last_60_days.reshape(1, sequence_length, 1)
predictions_scaled = []

for _ in range(7):
    pred = model.predict(input_seq, verbose=0)[0,0]
    predictions_scaled.append(pred)
    input_seq = np.append(input_seq[:,1:,:], [[[pred]]], axis=1)

predictions = scaler.inverse_transform(np.array(predictions_scaled).reshape(-1,1))

# Display predicted prices
st.subheader("Predicted Closing Prices for Next 7 Days")
for i, price in enumerate(predictions, 1):
    st.write(f"Day {i}: NT$ {price[0]:.2f}")

# Plot historical + predicted WITHOUT pyplot
future_dates = pd.date_range(start=df['Date'].iloc[-1] + pd.Timedelta(days=1), periods=7)

fig = Figure(figsize=(10,6))
ax = fig.subplots()
ax.plot(df['Date'], close_prices, label='Historical Close Price')
ax.plot(future_dates, predictions, label='Predicted Next 7 Days', marker='o')
ax.set_xlabel('Date')
ax.set_ylabel('Price (NT$)')
ax.set_title(f'Stock Price Prediction for {company_name}')
ax.legend()

# Show plot in Streamlit
st.pyplot(fig)
