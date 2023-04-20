import pandas as pd
import numpy as np
from binance.client import Client
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize']=20,10

from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))

# Variables
# -- You can change the crypto pair ,the start date and the time interval below --
client = Client()
pair_symbol = "BTCUSDT"
time_interval = Client.KLINE_INTERVAL_1DAY
start_date = "01 january 2017"

# Fetch data
klinesT = client.get_historical_klines(pair_symbol, time_interval, start_date)

# Create dataframe
df = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])

# Drop unnecessary columns
df.drop(['close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'], axis=1, inplace=True)

# Convert columns to numeric
for col in df.columns:
    df[col] = pd.to_numeric(df[col])

# Convert dates to datetime
df = df.set_index(df['timestamp'])
df.index = pd.to_datetime(df.index, unit='ms')
del df['timestamp']

# Split the df to train set and test set and define the learning period
training_set = df.copy().loc["2017":"2021"]
test_set = df.copy().loc["2022":]
learn_period = 7

# Scale the training set
sc = MinMaxScaler(feature_range=(0, 1))
training_set_scaled = sc.fit_transform(training_set["close"].values.reshape(-1, 1))

# Initialize the input and output arrays
X_train = []
y_train = []

# Create training set arrays
for i in range(learn_period, len(training_set)):
    # Append learn_period values of the scaled training set to X_train as inputs
    X_train.append(training_set_scaled[i-learn_period:i, 0])
    # Append the next value in the scaled training set to y_train as the output
    y_train.append(training_set_scaled[i, 0])

# Convert the arrays to numpy arrays
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshape the input arrays to be compatible with LSTM model
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Create a sequential model for predicting stock prices
lstm_model = Sequential()

# Add the first LSTM layer with 50 units, return_sequences=True, and input_shape as the shape of our training data
lstm_model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))

# Add a Dropout layer with a rate of 0.2 to prevent overfitting
lstm_model.add(Dropout(0.2))

# Add another LSTM layer with 50 units and return_sequences=True
lstm_model.add(LSTM(units=50, return_sequences=True))
lstm_model.add(Dropout(0.2))

# Add another LSTM layer with 50 units and return_sequences=True
lstm_model.add(LSTM(units=50, return_sequences=True))
lstm_model.add(Dropout(0.2))

# Add a final LSTM layer with 50 units
lstm_model.add(LSTM(units=50))
lstm_model.add(Dropout(0.2))

# Add a Dense layer with 1 unit to produce a single output value
lstm_model.add(Dense(units=1))

# Compile the model using the Adam optimizer and mean squared error loss function
lstm_model.compile(optimizer='adam', loss='mean_squared_error')
 
# Fit the model on the training data with 50 epochs and a 0
lstm_model.fit(X_train, y_train, epochs=50, batch_size=32)

# Get the actual stock price from the test set
real_stock_price = test_set.iloc[:, 1:2].values

# Combine the training and test sets to preprocess the inputs in the same way as the training set
dataset_total = pd.concat((training_set['close'], test_set['close']), axis = 0)

# Get the inputs from the combined dataset that correspond to the test set
inputs = dataset_total[len(dataset_total) - len(test_set) - learn_period:].values

# Reshape the inputs to have one column and apply feature scaling
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)

# Create the input data for the test set using the same sequence length as the training data
X_test = []
for i in range(learn_period, len(test_set) + learn_period):
    X_test.append(inputs[i-learn_period:i, 0])
X_test = np.array(X_test)

# Reshape the input data to fit the shape of the LSTM model input
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Use the trained LSTM model to predict the stock prices for the test set
predicted_stock_price = lstm_model.predict(X_test)

# Rescale the predicted stock prices back to the original scale
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

lstm_model.save("saved_lstm_model.h5")