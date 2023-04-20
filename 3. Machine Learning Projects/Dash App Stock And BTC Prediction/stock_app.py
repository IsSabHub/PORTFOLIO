import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from binance.client import Client
from dash.dependencies import Input, Output
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np


app = dash.Dash()
server = app.server

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

model=load_model("saved_lstm_model.h5")

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
predicted_stock_price = model.predict(X_test)

# Rescale the predicted stock prices back to the original scale
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# Set all values in the "predicted" column to 0
df["predicted"] = 0

# Replace the last n values in the "predicted" column with the predicted values 
# where n is the length of the predicted_stock_price array
df.loc[df.index[-len(predicted_stock_price.flatten()):], "predicted"] = predicted_stock_price.flatten()

# Calculate the difference between consecutive values in the "close" column
df["diff_close"] = df["close"].diff()

# Calculate the difference between consecutive values in the "predicted" column
df["diff_predicted"] = df["predicted"].diff()

# Shift the values in the "predicted" column up by 1
df["next_predicted"] = df["predicted"].shift(-1)

# Shift the values in the "close" column up by 1
df["next_close"] = df["close"].shift(-1)

# Calculate the difference between the next value in the "predicted" column and the current value
df["diff_predicted_next"] = df["next_predicted"] - df["predicted"]

# Calculate the difference between the next value in the "close" column and the current value
df["diff_close_next"] = df["next_close"] - df["close"]

# Calculate the mean evolution of the close price over the next 3, 5, 10, and 20 time steps
df["mean_evol_3"] = df["close"].shift(-3).rolling(3).mean() - df["close"]
df["mean_evol_5"] = df["close"].shift(-5).rolling(5).mean() - df["close"]
df["mean_evol_10"] = df["close"].shift(-10).rolling(10).mean() - df["close"]
df["mean_evol_20"] = df["close"].shift(-20).rolling(20).mean() - df["close"]


df_stock= pd.read_csv("./stock_data.csv")

app.layout = html.Div([
   
    html.H1("Stock Price Analysis Dashboard", style={"textAlign": "center"}),
   
    dcc.Tabs(id="tabs", children=[
       
        dcc.Tab(label='BTC-USD Data',children=[
            html.Div([
                html.H2("Actual closing price",style={"textAlign": "center"}),
                dcc.Graph(
                    id="Actual Data",
                    figure={
                        "data":[
                            go.Scatter(
                                x=df.index,
                                y=real_stock_price.flatten(),
                                mode='lines',
                                name='Actual Price'
                            )

                        ],
                        "layout":go.Layout(
                            title='Actual Price',
                            xaxis_title='Time (in periods)',
                            yaxis_title='Price'
                        )
                    }

                ),
                html.H2("LSTM Predicted closing price",style={"textAlign": "center"}),
                dcc.Graph(
                    id="Predicted Data",
                    figure={
                        "data":[
                            go.Scatter(
                                x=df.index,
                                y=df['predicted'],
                                mode='lines',
                                name='Predicted Price'
                            )

                        ],
                        "layout":go.Layout(
                            title='Price Prediction',
                            xaxis_title='Time (in periods)',
                            yaxis_title='Price',
                            xaxis=dict(range=['2022-01-02', df.index[-1]])
						)
					}

				)				
			])        		
        ]),
        dcc.Tab(label='Facebook Stock Data', children=[
            html.Div([
                html.H1("Stocks High vs Lows", 
                        style={'textAlign': 'center'}),
              
                dcc.Dropdown(id='my-dropdown',
                             options=[{'label': 'Tesla', 'value': 'TSLA'},
                                      {'label': 'Apple','value': 'AAPL'}, 
                                      {'label': 'Facebook', 'value': 'FB'}, 
                                      {'label': 'Microsoft','value': 'MSFT'}], 
                             multi=True,value=['FB'],
                             style={"display": "block", "margin-left": "auto", 
                                    "margin-right": "auto", "width": "60%"}),
                dcc.Graph(id='highlow'),
                html.H1("Stocks Market Volume", style={'textAlign': 'center'}),
         
                dcc.Dropdown(id='my-dropdown2',
                             options=[{'label': 'Tesla', 'value': 'TSLA'},
                                      {'label': 'Apple','value': 'AAPL'}, 
                                      {'label': 'Facebook', 'value': 'FB'},
                                      {'label': 'Microsoft','value': 'MSFT'}], 
                             multi=True,value=['FB'],
                             style={"display": "block", "margin-left": "auto", 
                                    "margin-right": "auto", "width": "60%"}),
                dcc.Graph(id='volume')
            ], className="container"),
        ])


    ])
])







@app.callback(Output('highlow', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown):
    dropdown = {"TSLA": "Tesla","AAPL": "Apple","FB": "Facebook","MSFT": "Microsoft",}
    trace1 = []
    trace2 = []
    for stock in selected_dropdown:
        trace1.append(
          go.Scatter(x=df_stock[df_stock["Stock"] == stock]["Date"],
                     y=df_stock[df_stock["Stock"] == stock]["High"],
                     mode='lines', opacity=0.7, 
                     name=f'High {dropdown[stock]}',textposition='bottom center'))
        trace2.append(
          go.Scatter(x=df_stock[df_stock["Stock"] == stock]["Date"],
                     y=df_stock[df_stock["Stock"] == stock]["Low"],
                     mode='lines', opacity=0.6,
                     name=f'Low {dropdown[stock]}',textposition='bottom center'))
    traces = [trace1, trace2]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                            '#FF7400', '#FFF400', '#FF0056'],
            height=600,
            title=f"High and Low Prices for {', '.join(str(dropdown[i]) for i in selected_dropdown)} Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': True}, 'type': 'date'},
             yaxis={"title":"Price (USD)"})}
    return figure


@app.callback(Output('volume', 'figure'),
              [Input('my-dropdown2', 'value')])
def update_graph(selected_dropdown_value):
    dropdown = {"TSLA": "Tesla","AAPL": "Apple","FB": "Facebook","MSFT": "Microsoft",}
    trace1 = []
    for stock in selected_dropdown_value:
        trace1.append(
          go.Scatter(x=df_stock[df_stock["Stock"] == stock]["Date"],
                     y=df_stock[df_stock["Stock"] == stock]["Volume"],
                     mode='lines', opacity=0.7,
                     name=f'Volume {dropdown[stock]}', textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data, 
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                            '#FF7400', '#FFF400', '#FF0056'],
            height=600,
            title=f"Market Volume for {', '.join(str(dropdown[i]) for i in selected_dropdown_value)} Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M',
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': True}, 'type': 'date'},
             yaxis={"title":"Transactions Volume"})}
    return figure



if __name__=='__main__':
	app.run_server(debug=True)