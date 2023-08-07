import csv, sys

def cusipLookup(ticker):
    file = "C:/Users/mcgra/OneDrive/Desktop/AHM Docs/Coding/Project/ProjectFiles/SECDocs/output.csv"
    # file = "C:/Users/mcgra/Documents/coding/Holdings/secholdings/output.csv"
    with open(file, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            if row[4] == ticker.upper():
                return row[0].upper().zfill(9)

if __name__ == "__main__":
    ticker = sys.argv[1].upper()
    print(cusipLookup(ticker))