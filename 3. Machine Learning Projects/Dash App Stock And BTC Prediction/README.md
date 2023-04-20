Cryptocurrency Price Prediction using LSTM Neural Networks

This project uses an LSTM (Long Short-Term Memory) neural network to predict the price of a cryptocurrency. The LSTM model is trained on historical price data for the cryptocurrency, and then used to predict the price for a future period.

The cryptocurrency data is obtained using the Binance API, which provides access to historical price data for a wide variety of cryptocurrencies, which can be changed by any other cryptocurrency pair in the code apps.

The data is preprocessed and split into a training set and a test set. The LSTM model is trained on the training set and used to predict the price for the test set.


The project is implemented using Python and the following libraries:

Dash: for creating a web-based user interface for the project
pandas: for data processing and manipulation
Plotly: for data visualization
Keras: for building the LSTM model
Scikit-learn: for data preprocessing and scaling
Binance API: for accessing historical cryptocurrency price data

Installation

To run this project on your local machine, you will need to have Python 3.x installed along with the following libraries:

pip install dash pandas plotly keras scikit-learn python-binance

Usage
To run the project, navigate to the project directory and run the following command:

python stock_pred.py

this will train the LSTM model on the historical price data and then use the model to predict the price for the test set. The results will save the model to "saved_lstm_model.h5"

and then run the following command:

python stock_app.py

This will start the Dash web application, which can be accessed by opening a web browser and navigating to http://localhost:8050.

The web application allows the user to select the cryptocurrency pair, start date, and time interval for the historical price data. The user can also select the number of days to use for learning when training the LSTM model.

After selecting the desired options, the user can click the "Predict" button to generate a graph of the predicted cryptocurrency price for the selected time period.