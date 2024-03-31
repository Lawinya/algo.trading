from flask import Flask, render_template
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)

# Function to fetch data and generate plot
def generate_plot():
    # Fetch intraday data for the stock (AAPL)
    stock = yf.Ticker("AAPL")
    data = stock.history(period="1d", interval="1m")

    # Calculate momentum
    data['momentum'] = data['Close'].pct_change()

    # Creating subplots to show momentum and buying/selling markers
    figure = make_subplots(rows=2, cols=1)
    figure.add_trace(go.Scatter(x=data.index, 
                             y=data['Close'], 
                             name='Close Price'))
    figure.add_trace(go.Scatter(x=data.index, 
                             y=data['momentum'], 
                             name='Momentum', 
                             yaxis='y2'))

    # Adding the buy and sell signals
    figure.add_trace(go.Scatter(x=data.loc[data['momentum'] > 0].index, 
                             y=data.loc[data['momentum'] > 0]['Close'], 
                             mode='markers', name='Buy', 
                             marker=dict(color='green', symbol='triangle-up')))

    figure.add_trace(go.Scatter(x=data.loc[data['momentum'] < 0].index, 
                             y=data.loc[data['momentum'] < 0]['Close'], 
                             mode='markers', name='Sell', 
                             marker=dict(color='red', symbol='triangle-down')))

    figure.update_layout(title='Algorithmic Trading using Momentum Strategy',
                      xaxis_title='Date',
                      yaxis_title='Price')
    figure.update_yaxes(title="Momentum", secondary_y=True)

    # Convert Plotly figure to JSON for embedding in HTML
    plot_json = figure.to_json()

    return plot_json

# Route for home page
@app.route('/')
def home():
    # Generate plot
    plot_json = generate_plot()
    return render_template('index.html', plot_json=plot_json)

if __name__ == '__main__':
    app.run(debug=True)
