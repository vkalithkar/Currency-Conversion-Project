import numpy as np
import pandas as pd

def get_countrycurrency_dicts(exchange_df: pd.DataFrame):
    country_to_currency = (exchange_df.groupby("country")["currency_name"].unique().apply(list).to_dict())
    currency_to_country = {currency: country
                           for country, currencies in country_to_currency.items()
                           for currency in currencies}
    return country_to_currency, country_to_currency

def get_country_data(exchange_df: pd.DataFrame, price_country: str):
    country_subset_df = exchange_df[exchange_df["country"] == price_country]
    x = country_subset_df["year"]
    y = country_subset_df['exchange_rate']
    return x, y