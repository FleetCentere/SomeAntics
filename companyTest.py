import requests, json, sys, random
from datetime import datetime

# define headers dictionary for SEC API
headers = {"User-Agent": "mcgrathan@gmail.com"}

# get company tickers from SEC API with headers and convert into JSON format
tickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()
max = len(tickers)

def main(ticker):
    # get company CIK from "tickers" file
    CIK = []
    for row in tickers:
        if tickers[row]["ticker"] == ticker.upper():
            CIK.append(str(tickers[row]["cik_str"]).zfill(10))

    # CIK is a list with only one element based on when the given ticker matches the ticker of the 'tickers' json returned from SEC
    cik_str = CIK[0]

    # company_submissions = requests.get(f"https://data.sec.gov/submissions/CIK{cik_str}.json", headers=headers).json()
    # company_concept = requests.get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_str}.json", headers=headers).json()
    company_facts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_str}.json", headers=headers).json()
    
    # determine what accounting format is used for given company in variable 'accounting'
    accounting = "na"
    for j, name in enumerate(list(company_facts["facts"].keys())):
        if name == "us-gaap" or name == "ifrs-full":
            accounting = name

    test = "CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization"

    output = company_facts["facts"][accounting][test]["units"]["USD"]

    return output

if __name__ == "__main__":
    
    # debugging:
    # ticker = "SES"
    # lists, facts, companyName = main(ticker)
    
    if len(sys.argv) == 2:
        output = main(sys.argv[1])
        for fact in output:
            print(fact)

    else:
        default = "MSFT"
        output = main(default)
        for fact in output:
            print(fact)