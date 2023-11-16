import yfinance as yf
import sys
import datetime

def sp500(ticker=None):
    class Price:
        def __init__(self, date, price):
            self.date = date
            self.price = price

    try:    
        # Create a ticker object for the S&P 500
        if ticker is None:
            y_ticker = yf.Ticker("^GSPC")
        else:
            y_ticker = yf.Ticker(ticker)
        # Get historical data for the security
        companyData = y_ticker.history(period="4d")

        # Get historical data for S&P500 as proxy for dates to use for Company
        spTicker = yf.Ticker("^GSPC")
        spData = spTicker.history(period="4d")
        numberOfDates = len(spData.index)

        # Get the Last Date that the S&P 500 has data
        last_date = spData.index[numberOfDates-1].date()

        # Get dates based on S&P info
        dates = []
        for i, row in enumerate(spData):
            dates.append(spData.index[i].date())

        dates = dates[-3:]
        priceOutput = []

        for date in dates:
            for i, row in enumerate(companyData['Close']):
                dayDate = companyData['Close'].index[i].date()
                if date == dayDate:
                    datum_date = date
                    try:
                        datum_price = companyData['Close'].iloc[i]
                    except:
                        datum_price = companyData['Close'].iloc[i-1]
                    datum = Price(datum_date, datum_price)
                    priceOutput.append(datum)
        return priceOutput
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