import requests, json, sys

def financials_search(ticker):
    # define headers dictionary for SEC API
    headers = {"User-Agent": "mcgrathan@gmail.com"}

    # get company tickers from SEC API with headers and convert into JSON format
    tickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()

    # get company CIK from "tickers" file
    CIK = []
    for row in tickers:
        if tickers[row]["ticker"] == ticker:
            CIK.append(str(tickers[row]["cik_str"]).zfill(10))
    
    cik_str = CIK[0]
    
    company_submissions = requests.get(f"https://data.sec.gov/submissions/CIK{cik_str}.json", headers=headers).json()
    # company_concept = requests.get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_str}.json", headers=headers).json()
    company_facts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_str}.json", headers=headers).json()

    i = 0
    accounting = "na"
    for j, name in enumerate(list(company_facts["facts"].keys())):
        if name == "us-gaap" or "ifrs-full":
            i = j
            accounting = name

    years = [2019, 2020, 2021, 2022]
    financials_list = ["Assets", "RevenueFromContractWithCustomerExcludingAssessedTax", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", 
            "CostOfRevenue", "DepreciationDepletionAndAmortization", "GeneralAndAdministrativeExpense", "GrossProfit", 
            "IncomeTaxExpenseBenefit", "Liabilities", "LongTermDebt", "NetCashProvidedByUsedInFinancingActivities", 
            "NetCashProvidedByUsedInInvestingActivities", "NetCashProvidedByUsedInOperatingActivities"]

    financials = {}
    for i in financials_list:
        financials[i] = {}
    
    for key in financials.keys():
        try: 
            source = company_facts["facts"][accounting][key]["units"]["USD"]
            for year in years:
                for row in source:
                    if row["fp"] == "FY" and row["fy"] == year:
                        financials[key][year] = format(round(row["val"]/1000000),",")
        except KeyError:
            financials[key] = "na"

    return financials, years


if len(sys.argv) == 1:
    ticker = "GENI"
else:
    ticker = sys.argv[1]


if __name__ == "__main__":
    table = financials_search(ticker)
    print(table)