'''
THis file will calculate execution metrics for the brokers who traded during this period

By Andrew McLaughlin
Last Updated: October 2025
'''

import pandas as pd
import argparse

def calculate_metrics(input_csv_file, output_metrics_file):
    '''
    Calculate execution metrics from FIX data CSV.'''
    df = pd.read_csv(input_csv_file, index_col="LastMkt")
    #calculate price improvement and average execution time for each LastMkt (broker)
    metrics = pd.DataFrame(index=df.index.unique())
    metrics['AvgExecSpeedSecs'] = df.groupby('LastMkt').apply(lambda x: (pd.to_datetime(x['ExecutionTransactTime']) - pd.to_datetime(x['OrderTransactTime'])).mean().total_seconds())
    metrics['AvgPriceImprovement'] = df.groupby('LastMkt').apply(lambda x: (x['LimitPrice'] - x['AvgPx']).mean())
    metrics.to_csv(output_metrics_file)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate execution metrics from trade data CSV.')
    parser.add_argument('input_csv_file', type=str, help='Path to the input FIX data CSV file.')
    parser.add_argument('output_metrics_file', type=str, help='Path to the output metrics file.')
    args = parser.parse_args()

    calculate_metrics(args.input_csv_file, args.output_metrics_file)
