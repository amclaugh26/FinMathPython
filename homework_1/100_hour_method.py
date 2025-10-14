'''
Function that takes a .fix file and converts it to a .csv file

Python for Financial Data Science
By Andrew McLaughlin

Last Updated: October 2025
'''

import argparse

                    

def fix_to_csv_old(input_file, output_file):
    '''
    takes a .fix file and returns a .csv file.

    [add all the caveats from the hw description here]

    Parameters:
    input_file (str): Path to the input .fix file.
    output_file (str): Path to the output .csv file.
    '''
# try:
    with open(input_file, 'r') as fix_file, open(output_file, 'w') as csv_file:
        fix_file = fix_file.readlines()  # Read all lines from the FIX file
        headers = "OrderID,OrderTransactTime,ExecutionTransactTime,Symbol,Side,OrderQty,LimitPrice,AvgPx,LastMkt"
        csv_file.write(headers + '\n')  # Write headers to the CSV file
        line_count = 0
        for line in fix_file: 
            line_count += 1
            print(f"Processing line {line_count}")
            cleaned_list = []
            FIX_message = line.split('\x01')  # Split the FIX message by the SOH character  
              # Check for Execution Report, ExecType=Trade, OrdStatus=Filled
            if ("35=8" in FIX_message) and ("150=2" in FIX_message) and ("39=2" in FIX_message) and ("40=2" in FIX_message):
               # match_found = 0
                order_time = "N/A"  # Default value if no match is found
                for order in fix_file:
                    order_message = order.split('\x01')
                
                      #check that order message is a new order single and that the ClOrdID matches the ExecID of the execution report
                    if ("35=D" in order_message) and (order_message[8]==FIX_message[9]):
                        #match_found = 1
                        order_time = order_message[15][3:]  # Extract Order Transact Time (tag 60)
                        print("MATCH FOUND")
                        for item in FIX_message:
                            if item.startswith("11=") or item.startswith("60=") or item.startswith("55=") or item.startswith("54=") or item.startswith("38=") or item.startswith("44=") or item.startswith("30="):
                                cleaned_list.append(item[3:]) #append the value after the '='
                            if item.startswith("6="):
                                cleaned_list.append(item[2:]) #append the value after the '='
                        ordered_list = [cleaned_list[1], order_time, cleaned_list[7], cleaned_list[6], cleaned_list[5], cleaned_list[3], cleaned_list[4], cleaned_list[0], cleaned_list[2]]
                        csv_line = ','.join(ordered_list) + '\n'
                        csv_file.write(csv_line)
                        match_found = 0  # Reset match_found for the next execution report
                    if order == line:
                        break  # Stop searching if we reach the execution report line again
                    
                ''' if match_found == 1:
                    for item in FIX_message:
                        if item.startswith("11=") or item.startswith("60=") or item.startswith("55=") or item.startswith("54=") or item.startswith("38=") or item.startswith("44=") or item.startswith("30="):
                            cleaned_list.append(item[3:]) #append the value after the '='
                        if item.startswith("6="):
                            cleaned_list.append(item[2:]) #append the value after the '='
                    ordered_list = [cleaned_list[1], order_time, cleaned_list[7], cleaned_list[6], cleaned_list[5], cleaned_list[3], cleaned_list[4], cleaned_list[0], cleaned_list[2]]
                    csv_line = ','.join(ordered_list) + '\n'
                    csv_file.write(csv_line)
                    match_found = 0  # Reset match_found for the next execution report
'''
               # if match_found == 0:
                #    print("No matching order found for this execution report.")
            else:
                pass
                #print("This line is not an execution report with ExecType=Trade and OrdStatus=Filled. Moving to the next line.")
                    
                                
                                
                        


   # except Exception as files_are_unable_to_be_converted_error:  
    #    print(f"The arguments passed are not able to be converted from .fix to .csv. Check your arguments to ensure they are compatible with the program")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert .fix file to .csv file')
    parser.add_argument('input_file', help='Path to the input .fix file')
    parser.add_argument('output_file', help='Path to the output .csv file')
    args = parser.parse_args()

    fix_to_csv_old(args.input_file, args.output_file)