from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
from datetime import datetime
import pytz

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    print(get_repo_path)
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    # Extract the timestamp value from the first row of the DataFrame
    #timestamp = df['timestamp'].iloc[0][:-9]
    datepart = df['timestamp'].iloc[0].split('T')[0]
    
    # Get the current timestamp in UTC timezone
    current_time_utc = datetime.utcnow()

    # Convert UTC to GMT+8 timezone
    gmt8 = pytz.timezone('Asia/Singapore')
    current_time_gmt8 = current_time_utc.astimezone(gmt8)

    # Format the current timestamp in GMT+8 timezone
    formatted_time_gmt8 = current_time_gmt8.strftime("%Y-%m-%dT%H:%M")

    # Print the formatted timestamp
    print("Current timestamp (YYYY-MM-DDTHH:MM):", formatted_time_gmt8)
    bucket_name = 'sg-car-parking'
    object_key = f'sgcp-{datepart}/sgcp-{formatted_time_gmt8}.csv'

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )