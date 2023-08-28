import yfinance as yf

def sp500():
    # Create a ticker object for the S&P 500
    sp500_ticker = yf.Ticker("^GSPC")

    # Get historical data for the S&P 500
    sp500_data = sp500_ticker.history(period="1d")

    # Get the last closing price
    last_close_price = sp500_data['Close'].iloc[-1]

    return last_close_price

    # print(f"The last closing price of the S&P 500 is ${last_close_price:.2f}")

if __name__ == "__main__":
    sp500()