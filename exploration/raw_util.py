import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def clean_trace(trace):
    """
    Load and import a single trace into a pandas DataFrame

    Parameters:
    -----------
    trace : str, path to the trace to be loaded

    Returns
    -------
    df : pandas DataFrame
        Cleaned single trace data
    """

    df = pd.read_csv(trace, delimiter=' ', header=None)
    
    # Meaningful column names
    df.columns = ['Timestamp', 'Direction', 'dummy1', 'Circuit', 
                  'dummy2', 'Stream', 'dummy3', 'Command',
                  'dummy4', 'Length']

    # Drop unnecessary columns
    df.drop(['dummy1', 'dummy2', 'dummy3', 'dummy4'], axis=1, inplace=True)

    # Dump trash commas and fix data types
    df['Circuit'] = df['Circuit'].apply(lambda x: x.rstrip(',')).astype('int')
    df['Stream'] = df['Stream'].apply(lambda x: x.rstrip(',')).astype('int')
    df['Command'] = df['Command'].apply(lambda x: x.rstrip(','))
    
    # Make an elapsed time in seconds column
    df['Elapsed Time'] = df['Timestamp'] - df['Timestamp'].iloc[0]
    return df
