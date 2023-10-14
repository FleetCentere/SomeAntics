import yfinance as yf
import sys

def sp500(ticker=None):
    try:    
        # Create a ticker object for the S&P 500
        if ticker is None:
            y_ticker = yf.Ticker("^GSPC")
        else:
            y_ticker = yf.Ticker(ticker)
        # Get historical data for the S&P 500
        data = y_ticker.history(period="3d")

        # Get the last closing price
        closes = data['Close'].iloc[-3]
        
        return data['Close'].iloc[-3:] # returns 3 prices in a row in order of t-2, t-1, t
    except Exception as e:
        return ["na"]
if __name__ == "__main__":
    if len(sys.argv) == 2:
        ticker = sys.argv[1].upper()
    else:
        ticker = None
    prices = sp500(ticker)
    print(prices)
    print("\n")
    for i in prices:
        print(i)
    print("\n")
    print(len(prices))