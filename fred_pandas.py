import os
import requests
import pandas as pd

# ----------------------------------------------------------------------
def download_series_after(series, observation_start=None):

    url = 'https://api.stlouisfed.org/fred/series/observations'

    if observation_start is None:
        params = {'series_id': series, 'file_type': 'json', 'api_key': os.environ['FRED_API_KEY'] }
    else:
        params = {'series_id': series, 'file_type': 'json', 'observation_start': observation_start, 'api_key': os.environ['FRED_API_KEY'] }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f'status_code: {response.status_code}.')
    else:
        df = pd.DataFrame(response.json()['observations'])
        print(f'Downloaded {len(df)} records.')
        return df
# ----------------------------------------------------------------------
def update_records(series, observation_start=None):

    path = f'{series}.pkl'

    if os.path.isfile(path):

        print(f'Found {path}. Importing.')

        df = pd.read_pickle(path)

        recent_date = df['date'].iloc[-2]

        print(f'Second most recent date: {recent_date}')

        new_records = download_series_after(series, recent_date)

        existing_records = df[df['date'] < recent_date]

        new_df = pd.concat([existing_records, new_records], ignore_index=True)

        new_df.to_pickle(path)

        return new_df

    else:

        print(f'Using observation_start={observation_start}.')

        df = download_series_after(series, observation_start)

        df.to_pickle(path)

        return df
# ----------------------------------------------------------------------
