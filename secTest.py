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
    try:
        company_facts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_str}.json", headers=headers).json()
    except requests.exceptions.JSONDecodeError:
        return ["list error"], ["facts error"], ticker
    companyName = company_facts["entityName"]

    # determine what accounting format is used for given company in variable 'accounting'
    accounting = "na"
    for j, name in enumerate(list(company_facts["facts"].keys())):
        if name == "us-gaap" or name == "ifrs-full":
            accounting = name

    # cash
    cash = ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
            "CashAndCashEquivalentsAtCarryingValue",
            "Cash"]
    
    # assets
    assets = ["Assets"]

    # liabilities
    liabilities = ["Liabilities"]

    # debt
    debt = ["LongTermDebt"]

    # revenue
    revenue = ["RevenueFromContractWithCustomerExcludingAssessedTax",
                "Revenues",
                "InterestIncomeExpenseNet",
                "Revenue"]

    # COGS
    cogs = ["CostOfGoodsAndServicesSold",
            "CostOfRevenue",
            "CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization"]

    # grossprofit
    grossprofit = ["GrossProfit"]

    # CFO
    cfo = ["NetCashProvidedByUsedInOperatingActivities"]

    # CFI
    cfi = ["NetCashProvidedByUsedInInvestingActivities"]

    # CFF
    cff = ["NetCashProvidedByUsedInFinancingActivities"]

    # order based on output: cash, assets, liabilities, debt, rev, cogs, gp, cfo, cfi, cff
    lists = [cash, assets, liabilities, debt, revenue, cogs, grossprofit, cfo, cfi, cff]
    
    maxYear = 2022
    # # i is an element of lists (cash, revenue, etc); j is an element of the [cash, revenue] list
    for n, i in enumerate(lists):
        for j in i:
            try:
                test = company_facts["facts"][accounting][j]["units"]["USD"]
                for row in test:
                    if row["fy"] == maxYear:
                        lists[n] = j
                        break
            except KeyError:
                lists[n] = "na"
                pass
    facts = company_facts["facts"][accounting]

    return lists, facts, companyName

if __name__ == "__main__":
    
    # debugging:
    # ticker = "SES"
    # lists, facts, companyName = main(ticker)
    
    if len(sys.argv) == 2:
        lists, facts, companyName = main(sys.argv[1])
        for fact in facts:
            print(fact)
        print("")
        print(companyName + ": ", end="")
        print(lists)
        # print(facts)

    else:
        number = 10 # number of random companies to generate keys
        randoms = [] # list to holder the random numbers
        randomTickers = [] # list of tickers corresponding to the random numbers
        for i in range(number):
            randomNumber = random.randint(0,max-1) # generate a random number between 0 and max-1 (of tickers json)
            randoms.append(randomNumber) # add random number to [randoms]
            randomTicker = tickers[str(randomNumber)]["ticker"] # get ticker based on random number
            randomTickers.append(randomTicker) # add ticker to [randomTickers]
        
        for ticker in randomTickers:
            lists, facts, companyName = main(ticker)
            print(companyName + "(" + ticker + "): ", end="")
            print(lists)