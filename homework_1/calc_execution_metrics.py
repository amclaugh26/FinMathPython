'''
THis file will calculate execution metrics for the brokers who traded during this period

By Andrew McLaughlin
Last Updated: October 2025
'''

import pandas as pd
import numpy as np
import argparse

def calculate_metrics(input_csv_file, output_metrics_file):
    '''
    Calculate execution metrics from FIX data CSV.
    
    Parameters:
    input_file (str): Path to the input .csv file.
    output_file (str): Path to the output .csv file.
    '''

    try:
        #read the csv 
        df = pd.read_csv(input_csv_file, index_col="LastMkt")

        #calculate speed
        df['ExecutionTransactTime'] = pd.to_datetime(df['ExecutionTransactTime'])
        df['OrderTransactTime'] = pd.to_datetime(df['OrderTransactTime'])
        df["exec_speed_secs"] = (df['ExecutionTransactTime'] - df['OrderTransactTime']).dt.total_seconds()

        #calculate price improvements
        df["price_improvement"] = np.where(df['Side']==1, df['LimitPrice'] - df['AvgPx'], df['AvgPx'] - df['LimitPrice'])

        #generate metrics dataframe
        metrics = pd.DataFrame(index=df.index.unique())
        metrics['AvgExecSpeedSecs'] =df.groupby('LastMkt')['exec_speed_secs'].mean()
        metrics['AvgPriceImprovement'] = df.groupby('LastMkt')['price_improvement'].mean()

        #publish to csv
        metrics.to_csv(output_metrics_file)
    
    except Exception as metric_error:  
        print(f"Unable to calculate metrics with files provided, ensure input csv has correct headings")





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate execution metrics from trade data CSV.')
    parser.add_argument('input_csv_file', type=str, help='Path to the input FIX data CSV file.')
    parser.add_argument('output_metrics_file', type=str, help='Path to the output metrics file.')
    args = parser.parse_args()

    calculate_metrics(args.input_csv_file, args.output_metrics_file)
