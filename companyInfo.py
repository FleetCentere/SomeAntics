import requests, json, random
import csv, sys
from ProjectFiles.api_keys import sec_headers

def getInfo(ticker):
    # define headers dictionary for SEC API
    headers = sec_headers

    # get company tickers from SEC API with headers and convert into JSON format
    tickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()
    for row in tickers:
        if tickers[row]["ticker"] == ticker.upper():
            CIK = str(tickers[row]["cik_str"]).zfill(10)
            break
    # company_submissions = requests.get(f"https://data.sec.gov/submissions/CIK{cik_str}.json", headers=headers).json()
    companyFacts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json", headers=headers).json()
    return companyFacts

def getRandomTicker():
    # define headers dictionary for SEC API
    headers = {"User-Agent": "mcgrathan@gmail.com"}

    # get company tickers from SEC API with headers and convert into JSON format
    tickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()
    max = len(tickers)
    randomNumber = random.randint(0,max-1) # generate a random number between 0 and max-1 (of tickers json)
    randomTicker = tickers[str(randomNumber)]["ticker"] # get ticker based on random number
    return randomTicker

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
    ticker = getRandomTicker()
    companyFacts = getInfo(ticker)
    companyName = companyFacts['entityName']
    CIK = str(companyFacts['cik']).zfill(10)
    print(companyName + ": " + ticker + " / " + CIK)
    
    #get CUSIP from argument
    ticker = sys.argv[1].upper()
    print(cusipLookup(ticker))