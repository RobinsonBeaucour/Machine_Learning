import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import optuna

from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
color_pal = sns.color_palette()
pd.options.plotting.backend = "plotly"
plt.style.use('fivethirtyeight')

def Country_temperature(df,country):
    """
    This function returns a list of column names in the given dataframe that start with the specified country name.
    
    Args:
        df (pandas DataFrame): The dataframe to search for columns in.
        country (str): The country symbole (two letters) to search for in the column names.

    Returns:
        list: A list of column names in the dataframe that start with the specified country name.
    """
    list_col = []
    for col in df.columns:
        if col.startswith(country):
            list_col.append(col)
    return list_col

def create_time_features(df):
    """
    This function takes in a dataframe and returns a modified dataframe with additional features.
    The added features include: hour, day of week, quarter, month, year, day of year, day of month, and week of year.

    Args:
    df (pandas.DataFrame): The input dataframe.

    Returns:
        pandas.DataFrame: The modified dataframe with additional features.
    """
    df = df[[]].copy()
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    df['weekofyear'] = df.index.isocalendar().week.astype("int64")
    return df

def features_importance(model,return_='show'):
    """
    This function plots the importance of features in the given model and returns the plot or the figure object depending on the specified value of 'return_'.
    
    Args:
        model (model object): The model object to get feature importances from.
        return_ (str, optional): Specifies whether to show the plot or return the figure object. Defaults to 'show'.

    Returns:
        plotly.graph_objects.Figure: The figure object containing the plot, if 'return_' is set to 'fig'.
    """
    # Create an empty figure
    fig = go.Figure()
    
    # Get the feature importances and sort them in descending order
    dd = pd.DataFrame(data=model.feature_importances_,index=model.feature_names_in_,columns=['importance']).sort_values(by='importance',ascending=False)
    
    # Add a bar trace to the figure using the feature names as x values and the importances as y values
    fig.add_trace(
        go.Bar(
            x = dd.index,
            y = dd['importance']*100
        )
    )
    
    # Update the layout of the figure
    fig.update_layout(
        title = 'Importance of features',
        yaxis_title="%"
    )
    
    # Check if the 'return_' parameter is valid
    assert return_ in ['fig','show'], "return_ must be 'fig' or 'show'"
    
    # Show the plot if 'return_' is set to 'show'
    if return_=='show':
        fig.show()
        
    # Return the figure object if 'return_' is set to 'fig'
    if return_ == 'fig':
        return fig

def temperature_pca(TA,n_components,location='all',prefix=''):
    """
    This function performs principal component analysis (PCA) on the given temperature data and returns the transformed features as a dataframe.
    
    Args:
        TA (pandas DataFrame): The temperature data to perform PCA on.
        n_components (int): The number of principal components to keep.
        location (str, optional): The location to select temperature data for. Set to 'all' to use all locations. Defaults to 'all'.

    Returns:
        pandas DataFrame: A dataframe containing the transformed features. The columns are named as '{location}_PCA_{k}', where k is the component number. The index is the same as the input dataframe.
    """
    # Initialize a PCA object with the specified number of components
    pca = PCA(n_components=n_components)
    
    # Select all temperature data or data for a specific location
    if location=='all':
        features = pca.fit_transform(TA)
    else:
        features = pca.fit_transform(TA[Country_temperature(TA,location)])
        
    # Return the transformed features as a dataframe
    return pd.DataFrame(features,columns=[f"{prefix}_{location}_PCA_{k}" for k in range(1,features.shape[1]+1)],index=TA.index)

