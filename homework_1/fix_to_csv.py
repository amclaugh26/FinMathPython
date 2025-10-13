'''
Function that takes a .fix file and converts it to a .csv file

Python for Financial Data Science
By Andrew McLaughlin

Last Updated: October 2025
'''

import argparse

                    

def fix_to_csv(input_file, output_file):
    '''
    takes a .fix file and returns a .csv file.

    [add all the caveats from the hw description here]

    Parameters:
    input_file (str): Path to the input .fix file.
    output_file (str): Path to the output .csv file.
    '''
    try:

        with open(input_file, 'r') as fix_file, open(output_file, 'w') as csv_file:
            headers = "OrderID,OrderTransactTime,ExecutionTransactTime,Symbol,Side,OrderQty,LimitPrice,AvgPx,LastMkt"
            csv_file.write(headers + '\n')  # Write headers to the CSV file
            for line in fix_file:
                cleaned_list = []
                list = line.split('\x01')

                if "35=D" or ("35=8" and "150=2" and "39=2" and "40=2") in list:
                    for item in list:
                        if item.startswith("11=") or item.startswith("60=") or item.startswith("55=") or item.startswith("54=") or item.startswith("38=") or item.startswith("44=") or item.startswith("6=") or item.startswith("30="):
                           cleaned_list.append(item[3:]) #append the value after the '='
                    ordered_list = [cleaned_list[1], cleaned_list[7], cleaned_list[6], cleaned_list[5], cleaned_list[3], cleaned_list[4], cleaned_list[0], cleaned_list[2]]
                    csv_line = ','.join(ordered_list) + '\n'
                    csv_file.write(csv_line)    


    except Exception as files_are_unable_to_be_converted_error:  
        print(f"The arguments passed are not able to be converted from .fix to .csv. Check your arguments to ensure they are compatible with the program")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert .fix file to .csv file')
    parser.add_argument('input_file', help='Path to the input .fix file')
    parser.add_argument('output_file', help='Path to the output .csv file')
    args = parser.parse_args()

    fix_to_csv(args.input_file, args.output_file)