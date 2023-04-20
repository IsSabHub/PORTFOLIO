Stock Prediction App

This is a simple web application that uses the Prophet library to make stock price predictions for a selected dataset

For main.py, this code uses financial data to predict stock prices. The data is obtained using the yfinance library, which allows downloading historical stock data from Yahoo Finance. The user can select from a set of stock indices, and the program will download the corresponding data.

The downloaded data is in the form of a time series, with columns representing the date and various stock market metrics such as open, close, high, low, and volume. The program then uses the Prophet library to analyze the time series data and make predictions about future stock prices. Prophet is a time-series forecasting library developed by Facebook and is widely used for financial forecasting tasks.

The predicted values are plotted using the Plotly library, which provides interactive visualizations for web-based applications. The program generates two plots: the first displays the raw time series data, with the open and close values plotted over time, and the second displays the predicted values over a specified time period.

Overall, this program serves as a useful tool for anyone interested in financial analysis and stock market predictions. It can be used to gain insights into how various stock indices have performed historically, as well as to make informed decisions about future investments.

Installation

To run this app, you need to have the following packages installed:

streamlit
yfinance
prophet
plotly

To install these packages, run the following command:

pip install streamlit yfinance prophet plotly

Usage

To run the app, open a terminal and navigate to the directory where the app.py file is located. Then, run the following command:

streamlit run main.py

Once the app is running, you can select a stock dataset and choose the number of years to predict. The app will then display the raw data, the predicted data, and the forecast components.


There is a second app, main_2.py

This is another streamlit app that predicts the future prices of cryptocurrencies. The app allows users to select one of the seven supported cryptocurrencies and choose the number of years they want to predict the prices for. The app then loads the historical prices of the selected cryptocurrency from Yahoo Finance using the yfinance package, preprocesses the data, and uses the Facebook Prophet library to create a time series model and make predictions.

The app then displays the raw data and a plot of the historical prices using the plotly library. Next, it displays the predicted data and a plot of the forecasted prices for the selected cryptocurrency. Finally, it displays the components of the forecasted data such as trends, weekly and yearly seasonality, and holiday effects. The user can use the app to gain insights into the trends and patterns of the selected cryptocurrency and make informed investment decisions.

To run the app, open a terminal and navigate to the directory where the app.py file is located. Then, run the following command:

streamlit run main_2.py

Once the app is running, you can select a cryptocurrency and choose the number of years to predict. The app will then display the raw data, the predicted data, and the forecast components.