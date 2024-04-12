from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from google.cloud import storage
from datetime import timedelta, datetime
import os
import pandas as pd

    
@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Template for loading data from a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'sg-car-parking'
    # today's date
    datepart = datetime.now().date()
    print(datepart)
    
    start_time = datetime.strptime('00:00', '%H:%M')
    end_time = datetime.strptime('23:59', '%H:%M')

    # Initialize list to store timestamps
    timestamps = []

    # Generate timestamps with 15-minute intervals
    current_time = start_time
    while current_time <= end_time:
        timestamps.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=15)

    # Print the list of timestamps
    print(timestamps)

    dataframes = []
    for t in timestamps:
        # sgcp-2024-04-08T17:14:26+08:00.csv
        object_key = f'sgcp-{datepart}/sgcp-{datepart}T{t}.csv'
        print(object_key)
    
        df = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
            bucket_name,
            object_key,
        )
        dataframes.append(df)

    # Concatenate all DataFrames into one DataFrame
    merged_df = pd.concat(dataframes, ignore_index=True)
    return merged_df
