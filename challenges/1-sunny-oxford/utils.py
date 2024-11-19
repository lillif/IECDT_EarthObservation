import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#####################################################
# helper functions to create ML timeseries datasets #
#####################################################

def _timeseries_for_continuous_data(df: pd.DataFrame, 
                                    target_column: str,
                                    inputs_length: int = 3) -> tuple[np.ndarray, np.ndarray]:
    """
    Function to create a time series dataset from a DataFrame that contains continuous data (no temporal gaps).

    Args:
    df: DataFrame, the input data
    target_column: str, the name of the target column
    inputs_length: int, the length of the input sequences (default is 3)

    Returns:
    X: numpy array, the input sequences of length input_sequence_length
    y: numpy array, the target values for each input sequence which are the sun hours on the day after
    """
    assert inputs_length > 0, 'Input sequence length must be greater than 0'
    # Sort by date to ensure chronological order
    df = df.sort_values(by='date').reset_index(drop=True)
    
    X, y, y_date = [], [], []
    
    # Loop through the DataFrame and create sequences
    for i in range(inputs_length, len(df)):
        # Input: previous input_length days
        X.append(df[target_column].iloc[i-inputs_length:i].values)
        
        # Output: sun measurement on the day after
        y.append(df[target_column].iloc[i])

        # Date of the target value
        y_date.append(df['date'].iloc[i])
    
    # Convert to numpy arrays
    X = np.array(X)
    y = np.array(y)
    
    return X, y, y_date


def create_timeseries_dataset(df: pd.DataFrame, 
                              target_column: str = 'total_sun_per_day',
                              inputs_length: int = 3) -> tuple[np.ndarray, np.ndarray]:
    """
    Function to create a time series dataset from a DataFrame.
    
    Args:
    df: DataFrame, the input data
    target_column: str, the name of the target column

    Returns:
    X: numpy array, the input sequences of length input_sequence_length
    y: numpy array, the target values for each input sequence which are the sun hours on the day after
    """
    X, y, y_dates = [], [], []
    
    # Sort by date to ensure chronological order
    df = df.sort_values(by='date').reset_index(drop=True)
    
    # Group by year and month to avoid sequences spanning multiple months
    for _, monthly_df in df.groupby([df['date'].dt.year, df['date'].dt.month]):
        # Generate sequences within each month
        X_month, y_month, y_dates_month = _timeseries_for_continuous_data(monthly_df, target_column=target_column, inputs_length=inputs_length)
        
        # Append results to the overall dataset
        X.extend(X_month)
        y.extend(y_month)
        y_dates.extend(y_dates_month)
    
    # Convert to numpy arrays
    X = np.array(X)
    y = np.array(y)
    y_dates = np.array(y_dates)
    
    return X, y, y_dates

def get_test_train_split_df(df: pd.DataFrame, day_split: int = 23) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits a DataFrame into training and test sets based on a day of the month.

    Args:
    df: pd.DataFrame, the DataFrame to split
    day_split: int, the day of the month to split on (default is 23 which results in 82% training set, 18% test set)

    Returns:
    tuple, training set and test set DataFrames (df_train, df_test)
    """
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.day
    df_train = df[df['day'] <= day_split].copy().drop(columns=['day'])
    df_test = df[df['day'] > day_split].copy().drop(columns=['day'])
    return df_train, df_test


####################################################
# Helper functions to plot time series predictions #
####################################################

def plot_time_series_predictions(
        y_true, 
        y_dates, 
        y_pred_train,
        y_pred_test, 
        y_dates_train, 
        y_dates_test,
        xlim=(pd.Timestamp('2021-01-01'), pd.Timestamp('2021-03-01'))
    ):
    plt.figure(figsize=(12, 3))
    plt.plot(y_dates,
            y_true,
            '-x',
            label='Measurements',
            linewidth=1,
            markersize=4,
            markeredgewidth=1.5,)

    plt.plot(y_dates_train, y_pred_train, '*', label='Predicted (train)')
    plt.plot(y_dates_test, y_pred_test, '*', label='Predicted (test)')
    plt.xlim(xlim)
    plt.legend()