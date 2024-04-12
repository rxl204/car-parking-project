if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    data.columns = (data.columns
                        .str.replace(' ', '_')
                        .str.lower())
                        # Replace null values with 'null'
    data = data.fillna('null')
    data.drop(['unnamed:_0'], axis=1)

# Replace empty strings with 'null'
    data = data.replace('', 'null') 
    filtered_df = data[data.isnull().any(axis=1) | (data == '').any(axis=1)]
    print(filtered_df.shape)
    return data
