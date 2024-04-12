import io
import pandas as pd
from pandas import json_normalize
import requests
import json
import codecs

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = 'https://api.data.gov.sg/v1//transport/carpark-availability'
    response = requests.get(url)
    data = response.text
    # Remove the UTF-8 BOM if present
    if data.startswith('\ufeff'):
        data = codecs.decode(data.encode(), 'utf-8-sig')


    # Parse the string into a JSON object
    json_data = json.loads(data)
    
    # Convert the JSON object into a DataFrame
    # Flatten the nested JSON structure
    flat_data = []
    for item in json_data['items']:
        timestamp = item['timestamp']
        for carpark in item['carpark_data']:
            carpark_number = carpark['carpark_number']
            update_datetime = carpark['update_datetime']
            total_lots = carpark['carpark_info'][0]['total_lots']
            lot_type = carpark['carpark_info'][0]['lot_type']
            lots_available = carpark['carpark_info'][0]['lots_available']
            flat_data.append({'timestamp': timestamp, 'carpark_number': carpark_number, 'update_datetime': update_datetime, 'total_lots': total_lots, 'lot_type': lot_type, 'lots_available': lots_available})

    # Convert the flattened data into a DataFrame
    df = pd.DataFrame(flat_data)

    return df