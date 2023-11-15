import requests, json, random
import csv, sys
if "__main__" == __name__:
    from api_keys import sec_headers
else:
    from ProjectFiles.api_keys import sec_headers

def getInfo(ticker):
    file = "C:/Users/mcgra/OneDrive/Desktop/AHM Docs/Coding/Project/ProjectFiles/SECDocs/cusipLookup.csv"    
    with open(file, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if row[1] == ticker:
                CIK = str(row[0]).zfill(10)     
    # define headers dictionary for SEC API
    headers = sec_headers
    try:
        companyFacts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json", headers=headers).json()
    except:
        companyFacts = {'entityName': 'na'}
    return companyFacts

def getRandomTicker():
    file = "C:/Users/mcgra/OneDrive/Desktop/AHM Docs/Coding/Project/ProjectFiles/SECDocs/cusipLookup.csv"
    with open(file, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        number = sum(1 for row in reader)
    randomNumber = random.randint(0,number-1) # generate a random number between 0 and max-1 (of tickers json)
    with open(file, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i == randomNumber:
                randomTicker = row[1]
        return randomTicker

def cusipLookup(ticker):
    file = "C:/Users/mcgra/OneDrive/Desktop/AHM Docs/Coding/Project/ProjectFiles/SECDocs/cusipLookup.csv"
    with open(file, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row[1] == ticker.upper():
                return row[3].upper().zfill(9)

if __name__ == "__main__":
    ticker = getRandomTicker()
    companyFacts = getInfo(ticker)
    companyName = companyFacts['entityName']
    CIK = str(companyFacts['cik']).zfill(10)
    print(companyName + ": " + ticker + " / " + CIK)
    
    #get CUSIP from argument
    ticker = sys.argv[1].upper()
    print(cusipLookup(ticker))