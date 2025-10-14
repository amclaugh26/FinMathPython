'''
Function that takes a .fix file and converts it to a .csv file

Python for Financial Data Science
By Andrew McLaughlin

Last Updated: October 2025
'''

import argparse
import pandas as pd

                    

def fix_to_csv_pandas(input_file, output_file):
    '''
    takes a .fix file and returns a .csv file.

    [add all the caveats from the hw description here]

    Parameters:
    input_file (str): Path to the input .fix file.
    output_file (str): Path to the output .csv file.
    '''
    #create two tables, one for new order single messages and one for filled execution reports
    print("Opening File")
    with open(input_file, 'r') as fix_file, open(output_file, 'w') as csv_file:
        print('File Opened')
        fix_file = fix_file.readlines()  # Read all lines from the FIX file
        new_order_singles = pd.DataFrame(columns=["OrderID", "OrderTransactTime"])
        execution_reports = pd.DataFrame(columns=["OrderID", "ExecutionTransactTime", "Symbol", "Side", "OrderQty", "LimitPrice", "AvgPx", "LastMkt"])
        counter = 0
        print("Parsing File...")
        for line in fix_file:
            counter += 1
            if counter % 20000==0:
                print(f"...parsed {counter} rows")
            split_line = line.split('\x01')

            if "35=D" in line:
                #add to new order single table
                for item in split_line:
                    if item.startswith("11="):
                        clordid = item[3:]
                    if item.startswith("60="):
                        order_time = item[3:]
                new_row = pd.DataFrame({"OrderID": [clordid], "OrderTransactTime": [order_time]})
                new_order_singles = pd.concat([new_order_singles, new_row], ignore_index=True)
               # new_order_singles = new_order_singles.append({"OrderID": clordid, "OrderTransactTime": order_time}, ignore_index=True)
            if ("35=8" in split_line) and ("150=2" in split_line) and ("39=2" in split_line) and ("40=2" in split_line):
                #add to execution report table
                for item in split_line:
                    if item.startswith("11="):
                        clordid = item[3:]
                    if item.startswith("60="):
                        exec_time = item[3:]
                    if item.startswith("55="):
                        symbol = item[3:]
                    if item.startswith("54="):
                        side = item[3:]
                    if item.startswith("38="):
                        order_qty = item[3:]
                    if item.startswith("44="):
                        limit_price = item[3:]
                    if item.startswith("6="):
                        avg_px = item[2:]
                    if item.startswith("30="):
                        last_mkt = item[3:]
                new_row = pd.DataFrame({"OrderID": [clordid], "ExecutionTransactTime": [exec_time], "Symbol": [symbol], "Side": [side], "OrderQty": [order_qty], "LimitPrice": [limit_price], "AvgPx": [avg_px], "LastMkt": [last_mkt]})
                execution_reports = pd.concat([execution_reports, new_row], ignore_index=True)
                #execution_reports = execution_reports.append({"OrderID": clordid, "ExecutionTransactTime": exec_time, "Symbol": symbol, "Side": side, "OrderQty": order_qty, "LimitPrice": limit_price, "AvgPx": avg_px, "LastMkt": last_mkt}, ignore_index=True)
        #merge the two tables on ClOrdID
        print("completed parsing {counter}.")
        merged = pd.merge(execution_reports, new_order_singles, on="OrderID", how="inner")
        #reorder columns
        merged = merged[["OrderID", "OrderTransactTime", "ExecutionTransactTime", "Symbol", "Side", "OrderQty", "LimitPrice", "AvgPx", "LastMkt"]]
        merged.to_csv(output_file, index=False)
        print("CSV created")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert .fix file to .csv file')
    parser.add_argument('input_file', help='Path to the input .fix file')
    parser.add_argument('output_file', help='Path to the output .csv file')
    args = parser.parse_args()

    fix_to_csv_pandas(args.input_file, args.output_file)