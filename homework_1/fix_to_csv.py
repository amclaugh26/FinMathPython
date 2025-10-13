'''
Function that takes a .fix file and converts it to a .csv file

Python for Financial Data Science
By Andrew McLaughlin

Last Updated: October 2025
'''

import argparse

                    

def fix_to_csv(input_file, output_file):
    '''
    Convert a .fix file to a .csv file.

    Parameters:
    input_file (str): Path to the input .fix file.
    output_file (str): Path to the output .csv file.
    '''
    try:

        with open(input_file, 'r') as fix_file, open(output_file, 'w') as csv_file:
            for line in fix_file:
                # Replace the FIX delimiter (ASCII 1) with a comma
                csv_line = line.replace('\x01', ',')
                # Write the modified line to the CSV file
                csv_file.write(csv_line)    


    except Exception as files_are_unable_to_be_converted_error:  
        print(f"The arguments passed are not able to be converted from .fix to .csv. Check your arguments to ensure they are compatible with the program")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert .fix file to .csv file')
    parser.add_argument('input_file', help='Path to the input .fix file')
    parser.add_argument('output_file', help='Path to the output .csv file')
    args = parser.parse_args()

    fix_to_csv(args.input_file, args.output_file)