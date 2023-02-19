import streamlit as st
from datetime import datetime
import yfinance as yf
from prophet import Prophet
from plotly import graph_objects as go
from prophet.plot import plot_plotly, plot_cross_validation_metric
import pandas as pd
import numpy as np
from prophet.diagnostics import cross_validation, performance_metrics


currentdate = datetime.now().strftime("%Y-%m-%d")

def load_data(ticker,start_date,end_date):
    data = yf.download(ticker,start_date,end_date)
    data.reset_index(inplace=True)
    return data

def plot_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'],name="Open"))
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Adj Close'],name="Adj Close"))
    fig.layout.update(title_text="",xaxis_rangeslider_visible=True)
    return fig
    
st.set_page_config(
    page_title = 'Forecasting Stock Price Dashboard',
    page_icon = '?',
    layout = 'wide'
)
st.title("Forecasting Stock Price")

placeholder = st.empty()

with placeholder.container():
    with st.sidebar:
        ticker_symbol = st.text_input(label="Enter Ticker Symbol",value="AAPL")
        start_date = st.date_input(label="Start Date",value=pd.to_datetime("2016-01-01",format="%Y-%m-%d"),
                                min_value=pd.to_datetime("2016-01-01",format="%Y-%m-%d"),
                                max_value=pd.to_datetime(currentdate,format="%Y-%m-%d"))


        n_year = st.number_input(label="Enter number of year",min_value=1,max_value=4,value=1)

        n_day = n_year*365
        load_data_state = st.text("Loading data...")
        data = load_data(ticker_symbol,start_date,currentdate)
        load_data_state.text("Load data done!")

    # fig_col1, fig_col2 = st.columns(2)
    
    tab1, tab2 = st.tabs(["Time Series Forecasting - Prophet","Time Series Data"])
    
    with tab1:
        #st.subheader("Time Series Forecasting")
        df_train = data.loc[:,['Date','Adj Close']]
        df_train = df_train.rename(columns={'Date':"ds",'Adj Close':"y"})

        model = Prophet(daily_seasonality=True)
        model.fit(df_train)
        future = model.make_future_dataframe(periods=n_day)
        forecast = model.predict(future)

        st.markdown(f"Forecast {ticker_symbol} Closing Price for {n_year} years")
        fig1 = plot_plotly(model,forecast,figsize=(800,600))
        st.plotly_chart(fig1)

    with tab2:
        #st.subheader("Time Series")
        st.plotly_chart(plot_data())

# st.subheader("Raw data")
# st.write(data.tail())
    fig2_col1, tbl_col2 = st.columns(2)

    with fig2_col1:
        st.subheader("Forecast components")
        fig2 = model.plot_components(forecast,figsize=(10,20))
        st.write(fig2)

    with tbl_col2:
        st.subheader('Forecast data')
        st.write(forecast.tail())

        # perform cross validation
        df_cv = cross_validation(model, initial='730 days',period='180 days', horizon='365 days' )
        st.subheader("Cross Validation")
        st.write(df_cv.head())

        st.subheader('Performance Metric - RMSE')
        df_pm = performance_metrics(df_cv)  

        fig3 = plot_cross_validation_metric(df_cv,metric='rmse',figsize=(10,4.5)) 
        st.write(fig3)