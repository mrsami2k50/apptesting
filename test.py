import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # '3' means ERROR level only
# import tensorflow as tf
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import warnings
import streamlit as st

st.header("Hello....!!!")

# Ignore FutureWarnings and UserWarnings globally
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

# stock_no = '6753.TW'
# stock_no = '4749.TWO'
# stock_no = '3006.TW'
stock_no = '5234.TW'

# ticker = yf.Ticker(stock_no)
# info = ticker.info
# company_name = info.get("longName", "Name not available")

# Use:
company_name = "Lungteh Shipbuilding"  # hardcode

start_date = '2025-01-01'  # past date
end_date = '2026-05-30'    # today's date


## Download Lungteh Shipbuilding historical stock data from 2023-01-01 to today
df = yf.download(stock_no, start=start_date, end=end_date)
df = df.reset_index()
df.columns = df.columns.get_level_values(0)
df['Date'] = pd.to_datetime(df['Date'])

# Sort by Date (just in case)
df = df.sort_values('Date').reset_index(drop=True)

df = df.sort_values('Date')
df.reset_index(drop=True, inplace=True)

# Step 3: Prepare the closing prices
close_prices = df['Close'].values.reshape(-1,1)

# Step 4: Normalize the data (scale between 0 and 1)
scaler = MinMaxScaler(feature_range=(0,1))
close_scaled = scaler.fit_transform(close_prices)

# Step 5: Create sequences of 60 days for training
sequence_length = 60

def create_dataset(data, seq_length):
    xx = []
    yy = []
    for k in range(seq_length, len(data)):
        xx.append(data[k-seq_length:k, 0])
        yy.append(data[k,0])
    return np.array(xx), np.array(yy)

X, y = create_dataset(close_scaled, sequence_length)

# Reshape X to be [samples, time steps, features] for LSTM
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# Step 6: Build the LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

# Step 7: Train the model
model.fit(X, y, epochs=20, batch_size=32)

# Step 8: Predict the next 7 days (one week)
# Use the last 60 days data from dataset as input for prediction
last_60_days = close_scaled[-60:]
input_seq = last_60_days.reshape(1, sequence_length, 1)

predictions_scaled = []
# for _ in range(7):
    # pred = model.predict(input_seq, verbose=0)[0, 0]
    # predictions_scaled.append(pred)

    # pred_arr = np.array(pred, dtype=np.float32).reshape(1, 1, 1)

    # input_seq = np.concatenate(
        # (input_seq[:, 1:, :], pred_arr),
        # axis=1
    # )

for _ in range(7):
    pred = model.predict(input_seq)[0,0]
    predictions_scaled.append(pred)
    # Update the input_seq by removing first value and adding prediction
    input_seq = np.append(input_seq[:,1:,:], [[[pred]]], axis=1)

# Inverse transform to get actual prices
predictions = scaler.inverse_transform(np.array(predictions_scaled).reshape(-1,1))

# Step 9: Print predicted prices for next 7 days
st.write("Predicted closing prices for the next 7 days:")
for i, price in enumerate(predictions, 1):
    st.write(f"Day {i}: NT$ {price[0]:.2f}")

# Step 10: Plot the results
future_dates = pd.date_range(start=df['Date'].iloc[-1] + pd.Timedelta(days=1), periods=7)
plt.figure(figsize=(10,6))
plt.plot(df['Date'], close_prices, label='Historical Close Price')
plt.plot(future_dates, predictions, label='Predicted Next 7 Days', marker='o')
plt.xlabel('Date')
plt.ylabel('Price (NT$)')
plt.title(f'Stock Price Prediction for {company_name}')
plt.legend()

# Display the figure in Streamlit
st.pyplot(plt.gcf())
