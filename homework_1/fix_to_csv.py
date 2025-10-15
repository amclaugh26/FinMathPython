'''
Function that takes a .fix file and converts it to a .csv file

Python for Financial Data Science
By Andrew McLaughlin

Last Updated: October 2025
'''

import argparse
import pandas as pd
from collections import defaultdict

                    

def fix_to_csv(input_file, output_file):
    '''
    takes a .fix file and returns a .csv file.

    Parameters:
    input_file (str): Path to the input .fix file.
    output_file (str): Path to the output .csv file.
    '''
    #create two tables, one for new order single messages and one for filled execution reports
    
    try:
        print("Opening File")
        #open file
        with open(input_file, 'r') as fix_file:      
            print('File Opened')
            counter = 0
            orders = defaultdict(list)
            print("Parsing File...")


            #Line by line analysis
            for line in fix_file:

                #counter to check on progress (can comment out if unwanted)
                counter += 1
                if counter % 20000==0:
                    print(f"...parsed {counter} rows")

                #manipulate message to be easily readible by system
                fix_message = line.split('\x01')
                fix_dict = {code.split("=")[0]: code.split("=")[1] for code in fix_message if "=" in code}

                #create entries for new orders
                if fix_dict.get("35") == "D":
                    order_id = fix_dict.get("11")
                    order_time = fix_dict.get("60")
                    orders[order_id].append({'OrderID': order_id, 'OrderTransactTime': order_time})


                #find the fill for a new order
                if fix_dict.get("35") == "8" and fix_dict.get("150") == "2" and fix_dict.get("39") == "2" and fix_dict.get("40") == "2":
                    order_id = fix_dict.get("11")
                    if order_id in orders:              
                        exec_time = fix_dict.get("60")
                        symbol = fix_dict.get("55")
                        side = fix_dict.get("54")
                        order_qty = fix_dict.get("38")
                        limit_price = fix_dict.get("44")
                        avg_px = fix_dict.get("6")
                        last_mkt = fix_dict.get("30")
                        orders[order_id].append({'ExecutionTransactTime': exec_time, 'Symbol': symbol, 'Side': side, 'OrderQty': order_qty, 'LimitPrice': limit_price, 'AvgPx': avg_px, 'LastMkt': last_mkt})
            
            print("Completed parsing all rows\nConverting dictionaries to csv")

            # Flatten list of dicts per order_id (used google to help me with this)
            flattened_orders = {}
            for order_id, details_list in orders.items():
                combined = {}
                for d in details_list:
                    combined.update(d)  # merge all dictionaries
                flattened_orders[order_id] = combined

            #convert to dataframe and create csv
            df = pd.DataFrame.from_dict(flattened_orders, orient='index')
            df = df.dropna()            # Drop orders that were not filled
            df = df.reset_index(drop=True)
            df.to_csv(output_file, index=False)
            print(f"{output_file} created")
        
    except:  
        print("The arguments passed are not able to be converted from .fix to .csv. Check your arguments to ensure they are compatible with the program")


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='Convert .fix file to .csv file')
        parser.add_argument('--input_file', help='Path to the input .fix file.  For example, python homework_1/fix_to_csv.py --input_file data/cleaned.fix --output_file data/output_csv_file.csv')
        parser.add_argument('--output_file', help='Path to the output .csv file.  For example, python homework_1/fix_to_csv.py --input_file data/cleaned.fix --output_file data/output_csv_file.csv')
        args = parser.parse_args()

        fix_to_csv(args.input_file, args.output_file)

    except:
        print("Command lines arguments not provided. Ensure both an input and output file path are provided.  For example, python homework_1/fix_to_csv.py --input_file data/cleaned.fix --output_file data/output_csv_file.csv")
    
 