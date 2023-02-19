# Interactive Time Series Stock Price Prediction using Prophet

This repo contains files to build an interactive time series stock price forecasting web application using streamlit. 

Time series forecasting is the task of predicting future values based on historical data.  The interactive dashboard allows users to enter any stock ticker symbol, historical start date, number of year to make prediction.  Upon given selected parameters, the app run the prediction model using Prophet.    Prophet is a popular time series forecasting packages developed by Meta(Facebook) where non-linear trends are fit to seasonality effects such as daily, weekly, yearly and holiday trends.  It provide users with predicted futuer stock prices as well as the model performance.  

To install the required packages in the environment: 
```
pip install -r requirements.txt
```

To run the dashboard locally, use the command:
```
streamlit run myapp.py
```

![/StockPricePrediction.gif](https://github.com/ChristineLwin/Analytics_DashBoards/blob/main/Stock_Price_Prediction/spf_db.gif)
