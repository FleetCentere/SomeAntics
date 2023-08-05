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

    # determine what accounting format is used for given company in variable 'accounting'
    # i stores what nth key is the accounting key in the 'facts' dictionary
    i = 0
    accounting = "na"
    for j, name in enumerate(list(company_facts["facts"].keys())):
        if name == "us-gaap" or "ifrs-full":
            i = j
            accounting = name

    # generate a list storing the years for tracking
    years = []
    endYear = 2022
    if int(startYear) == int(endYear):
        years = [startYear]
    else:
        number = int(endYear) - int(startYear) + 1
        for i in range(number):
            years.append(int(startYear) + i)
    
    # list of desired financials to track
    financials_list = ["Assets", "RevenueFromContractWithCustomerExcludingAssessedTax", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", 
            "CostOfRevenue", "DepreciationDepletionAndAmortization", "GeneralAndAdministrativeExpense", "GrossProfit", 
            "IncomeTaxExpenseBenefit", "Liabilities", "LongTermDebt", "NetCashProvidedByUsedInFinancingActivities", 
            "NetCashProvidedByUsedInInvestingActivities", "NetCashProvidedByUsedInOperatingActivities"]

    # financials is a dictionary to store keys from financials_list with values of dictionaries for the years-values
    financials = {}
    for i in financials_list:
        financials[i] = {}
    
    for key in financials.keys():
        try: 
            source = company_facts["facts"][accounting][key]["units"]["USD"]
            for year in years:
                for row in source:
                    dateFormat = "%Y-%m-%d"
                    days = (datetime.strptime(row["end"], dateFormat) - datetime.strptime(row["start"], dateFormat)).days
                    if row["fp"] == "FY" and row["fy"] == year and 360 <= days <= 370:
                        financials[key][year] = format(round(row["val"]/1000000),",")
        except KeyError:
            financials[key] = "na"
    if __name__ == "__main__":
        rev_source = company_facts["facts"][accounting]["RevenueFromContractWithCustomerExcludingAssessedTax"]["units"]["USD"]
        # for row in rev_source:
        #     print(row)
        return financials, years, rev_source
    
    rev_source = company_facts["facts"][accounting]["RevenueFromContractWithCustomerExcludingAssessedTax"]["units"]["USD"]

    return financials, years


if len(sys.argv) == 1:
    ticker = "GENI"
else:
    ticker = sys.argv[1]

if __name__ == "__main__":
    startYear = 2018
    table = finSearch(ticker, startYear)
    print(table)