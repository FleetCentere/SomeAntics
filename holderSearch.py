import csv, sys
from ProjectFiles.companyInfo import cusipLookup

def holderSearch(ticker, c):
    infotable = "C:/Users/mcgra/OneDrive/Desktop/AHM Docs/Coding/Project/ProjectFiles/SECDocs/INFOTABLE.tsv"
    # infotable = "C:/Users/mcgra/Documents/coding/Holdings/secholdings/SECDocs/INFOTABLE.tsv"
    holderFile = "C:/Users/mcgra/OneDrive/Desktop/AHM Docs/Coding/Project/ProjectFiles/SECDocs/COVERPAGE.tsv"
    # holder_file = "C:/Users/mcgra/Documents/coding/Holdings/secholdings/SECDocs/COVERPAGE.tsv"
    CUSIP = cusipLookup(ticker)
    
    count = int(c)
    # extract rows with CUSIP equal to that of ticker in column 5 (row[4]) of reader output
    with open(infotable, "r") as infotable:
        reader = csv.reader(infotable, delimiter="\t")
        headers = next(reader)
        filtered_rows = []
        for row in reader:
            if (row[4].upper() == CUSIP.upper()): filtered_rows.append(row)
    
    if not filtered_rows:
        return headers, 0, CUSIP
    
    with open(holderFile, "r") as holderFile:
        holder_reader = csv.reader(holderFile, delimiter="\t")
        holder_dict = {row[0]: row[9] for row in holder_reader}

    sorted_rows = sorted(filtered_rows, key=lambda row: int(row[6]), reverse=True)
    
    sorted_table = []
    sorted_table.append(headers[:-7] + ["Holder Name"])
    height = 0
    for i, row in enumerate(sorted_rows):
        fund_id = row[0]
        fund_name = holder_dict.get(fund_id, "")
        prior_fund = sorted_table[height][7]
        if fund_name != prior_fund:
            sorted_table.append(row[:-7] + [fund_name])
            height += 1
        else:
            count += 1
        if i >= count-1:
            break
    
    sorted_simple_table = []
    sum = 0
    last_row = 0
    for i, row in enumerate(sorted_table[1:]):
        new_row = [i+1, row[7], format(int(row[6]), ",")]
        sorted_simple_table.append(new_row)
        sum = sum + int(row[6])
        last_row = i+1

    sorted_simple_table.append(["", "Total", format(sum,",")])
    return sorted_simple_table, last_row, CUSIP

# CUSIP = CUSIPSearch(ticker)
# count = 10
if __name__ == "__main__":
    count = 20
    ticker = "GDEVW"
    print(holderSearch(ticker, count))