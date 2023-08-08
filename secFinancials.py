import requests, json, sys
from datetime import datetime

def finSearch(ticker, startYear):
    # define headers dictionary for SEC API
    headers = {"User-Agent": "mcgrathan@gmail.com"}

    # get company tickers from SEC API with headers and convert into JSON format
    tickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()

    # get company CIK from "tickers" file
    CIK = []
    for row in tickers:
        if tickers[row]["ticker"] == ticker.upper():
            CIK.append(str(tickers[row]["cik_str"]).zfill(10))
    
    # CIK is a list with only one element based on when the given ticker matches the ticker of the 'tickers' json returned from SEC
    cik_str = CIK[0]
    
    company_submissions = requests.get(f"https://data.sec.gov/submissions/CIK{cik_str}.json", headers=headers).json()
    # company_concept = requests.get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_str}.json", headers=headers).json()
    company_facts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_str}.json", headers=headers).json()

    companyName = company_facts["entityName"]
    # sharesOut = company_facts["facts"]["dei"]["EntityCommonStockSharesOutstanding"]
    # floatOut = company_facts["facts"]["dei"]["EntityPublicFloat"]
    
    # determine what accounting format is used for given company in variable 'accounting'
    # i stores what nth key is the accounting key in the 'facts' dictionary
    accounting = "na"
    for j, name in enumerate(list(company_facts["facts"].keys())):
        if name == "us-gaap" or name == "ifrs-full":
            accounting = name

    # generate a list storing the years for tracking
    years = []
    endYear = 2023
    if int(startYear) == int(endYear):
        years = [startYear]
    else:
        number = int(endYear) - int(startYear) + 1
        for i in range(number):
            years.append(int(startYear) + i)
    
    # cash
    cash = ["CashCashEquivalentsAndShortTermInvestments",
            "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
            "CashAndCashEquivalentsAtCarryingValue",
            "Cash"]
    
    # assets
    assets = ["Assets"]

    # liabilities
    liabilities = ["Liabilities"]

    # debt
    debt = ["DebtInstrumentPrincipalOutstanding",
            "LongTermDebt",
            "DebtInstrumentFaceAmount",]

    # revenue
    revenue = ["RevenueFromContractWithCustomerExcludingAssessedTax",
                "Revenues",
                "InterestIncomeExpenseNet",
                "Revenue"]

    # COGS
    cogs = ["CostOfGoodsAndServicesSold",
            "CostOfRevenue"]

    # grossprofit
    grossprofit = ["GrossProfit"]

    # CFO
    cfo = ["NetCashProvidedByUsedInOperatingActivities"]

    # CFI
    cfi = ["NetCashProvidedByUsedInInvestingActivities"]

    # CFF
    cff = ["NetCashProvidedByUsedInFinancingActivities"]

    # order based on output: cash, assets, liabilities, debt, rev, cogs, gp, cfo, cfi, cff
    financialsList = [cash, assets, liabilities, debt, revenue, cogs, grossprofit, cfo, cfi, cff]

    # i is an element which is a list (cash list, revenue list, etc); j is an element of the i-th list [cash, revenue] list
    for n, i in enumerate(financialsList):
        for j in i:
            try:
                test = company_facts["facts"][accounting][j]
                financialsList[n] = j
                break
            except KeyError:
                financialsList[n] = "na"
                pass

    # financials is a dictionary to store keys from financials_list with values of dictionaries for the years-values
    financials = {}
    for i in financialsList:
        financials[i] = {}
    
    for key in financials.keys():
        try: 
            source = company_facts["facts"][accounting][key]["units"]["USD"]
            for year in years:
                for row in source:
                    dateFormat = "%Y-%m-%d"
                    try:
                        days = (datetime.strptime(row["end"], dateFormat) - datetime.strptime(row["start"], dateFormat)).days
                    except KeyError:
                        days = 365
                    if row["fp"] == "FY" and row["fy"] == year and 360 <= days <= 370:
                        financials[key][year] = "({:,})".format(abs(round(row["val"]/1000000))) if row["val"] < 0 else "{:,}".format(round(row["val"]/1000000))                        
        except KeyError:
            financials[key] = "na"
    
    if __name__ == "__main__":
        one_source = company_facts["facts"][accounting]["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]["units"]["USD"]
        for row in one_source:
            print(row)
        return companyName, financials, years, one_source
    
    # one_source = company_facts["facts"][accounting]["CashCashEquivalentsAndShortTermInvestments"]["units"]["USD"]

    # output wants to be companyName, financials, years
    return companyName, financials, years #, one_source


if len(sys.argv) == 1:
    ticker = "GENI"
else:
    ticker = sys.argv[1]

if __name__ == "__main__":
    startYear = 2018
    companyName, financials, years, one_source = finSearch(ticker, startYear)
    print(financials)