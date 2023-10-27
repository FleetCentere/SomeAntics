import requests, json, random

def getInfo(ticker):
    # define headers dictionary for SEC API
    headers = {"User-Agent": "mcgrathan@gmail.com"}

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

if __name__ == "__main__":
    ticker = getRandomTicker()
    companyFacts = getInfo(ticker)
    companyName = companyFacts['entityName']
    CIK = str(companyFacts['cik']).zfill(10)
    print(companyName + ": " + ticker + " / " + CIK)