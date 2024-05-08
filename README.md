# treasury_gov_pandas.py

Library for downloading FRED series data.

The first time you request a series, the data is retrieved and saved locally. Subsequent requests for the series only download newly available records plus a few others to ensure continuity.

