import requests, json, random
import csv, sys
if __name__ != "__main__":
    from ProjectFiles.api_keys import sec_headers

def main():
    # define headers dictionary for SEC API
    headers = sec_headers
    # get company tickers from SEC API with headers and convert into JSON format
    tickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()
    # print(tickers)
    with open('secTickersJSON.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Ticker", "CIK Code"])
        for i, company in enumerate(tickers):
            # if i > 5:
            #     break
            writer.writerow([tickers[company]['ticker'], tickers[company]['cik_str']])

def getCIK(ticker):
    headers = sec_headers
    tickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()
    for row in tickers:
        if tickers[row]["ticker"] == ticker.upper():
            CIK = str(tickers[row]["cik_str"]).zfill(10)
            break
    return CIK

def filingHistory(ticker):
    headers = sec_headers
    CIK = getCIK(ticker)
    filings = requests.get(f"https://data.sec.gov/submissions/CIK{CIK}.json", headers=headers).json()
    # print(filings)
    # print(filings['filings'])
    sec_base_url = "https://www.sec.gov/Archives/"
    keys = []
    for key in filings['filings']['recent'].keys():
        keys.append(key)
    keys.append("Link")
    # print(keys) #['accessionNumber', 'filingDate', 'reportDate', 'acceptanceDateTime', 'act', 'form', 'fileNumber', 'filmNumber', 'items', 'size', 'isXBRL', 'isInlineXBRL', 'primaryDocument', 'primaryDocDescription', 'Link']
    
    with open('companyFilings.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(keys)
        for i, number in enumerate(filings['filings']['recent']['accessionNumber']):
            row = []
            for key in keys[:-1]: #ending one element before the end due to the manual addition of "link" to generate a link
                element = filings['filings']['recent'][key][i]
                row.append(element)
            link = sec_base_url + "edgar/data/" + str(CIK) + "/" + number.replace("-", "") + "/" + number + "-index.htm"
            row.append(link)
            writer.writerow(row)
            if i == 0:
                last_filing = row
    # print(last_filing) # ['0001820872-23-000008', '2023-11-07', '2023-09-30', '2023-11-07T08:06:03.000Z', '34', '10-Q', '001-39576', '231381724', '', 8811754, 1, 1, 'gbtg-20230930.htm', '10-Q', 'https://www.sec.gov/Archives/edgar/data/0001820872/000182087223000008/0001820872-23-000008-index.htm']
    last_filing_url = last_filing[-1:]
    last_filing_date = last_filing[1:2]
    last_filing_type = last_filing[5:6]
    return last_filing_date[0], last_filing_url[0], last_filing_type[0]

if __name__ == "__main__":
    ticker = sys.argv[1].upper()
    from api_keys import sec_headers
    a, b = filingHistory(ticker)
    print(a)
    print(b)
