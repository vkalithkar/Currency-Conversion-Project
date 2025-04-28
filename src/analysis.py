import numpy as np
import pandas as pd

def get_country_exchange_data(exchange_df: pd.DataFrame, price_country: str):
    country_subset_df = exchange_df[exchange_df["country"] == price_country]
    x = country_subset_df["year"]
    y = country_subset_df['exchange_rate']
    return x, y

def get_country_crisis_data(crisis_df: pd.DataFrame, price_country: str):
    country_subset_df = crisis_df[crisis_df["country"] == price_country]
    return country_subset_df

def get_exchange_subset(exchange_df, country: str, currency: str, year: int):
    year = int(year)
    subset = exchange_df[
        (exchange_df['country'] == country) &
        (exchange_df['currency_name'] == currency) &
        (exchange_df['year'] == year)
    ]
    return subset