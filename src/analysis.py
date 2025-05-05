import pandas as pd

def get_country_exchange_data(exchange_df: pd.DataFrame, 
                              price_country: str) -> list:
    """
    Given a country, subset the exchange rate DataFrame into the Series of years for a that country and the 
    corresponding exchange rates. This function is used to create the exchange rate line graph figures.

    Arguments:
        exchange_df (pd.DataFrame): the full DataFrame of exchange data to subset.
        price_country (str): the selected country with which to subset the DataFrame by.
    
    Output:
        (list): the two pd.Series objects, the years for a given country and the corresponding exchange rates for 
                that country.
    """
    country_subset_df = exchange_df[exchange_df["country"] == price_country]

    # Set the soon-to-be axes to their corresponding Series
    x = country_subset_df["year"]
    y = country_subset_df['exchange_rate']

    return x, y

def get_country_crisis_data(crisis_df: pd.DataFrame, 
                            price_country: str) -> pd.DataFrame:
    """
    Given a country, subset the crisis DataFrame into the list of years for a that country and the corresponding 
    historical event points.

    Arguments:
        crisis_df (pd.DataFrame): the full DataFrame of crisis data to subset.
        price_country (str): the selected country with which to subset the DataFrame by.
    
    Output:
        country_subset_df (pd.DataFrame): the subsetted crisis DataFrame with data for the given country.
    """
    # Subset the crisis data to a given country's info
    country_subset_df = crisis_df[crisis_df["country"] == price_country]
    return country_subset_df

def get_exchange_rate_val(exchange_df: pd.DataFrame, 
                          country: str, 
                          currency: str, 
                          year: str) -> float:
    """
    Given a country, subset the exchange rate DataFrame into the given year, country, and currency to acquire the 
    exchange rate associated.

    This function is used to acquire the actual exchange rate during the submit-val callback.

    Arguments:
        exchange_df (pd.DataFrame): the full DataFrame of exchange data to subset.
        country (str): the selected country with which to subset the DataFrame by.
        currency (str): the selected currency with which to subset the DataFrame by.
        year (str): the selected year with which to subset the DataFrame by.
    
    Output:
        rate (float): the exchange rate value gathered from the exchange_df DataFrame for the given fields.
    """

    # Year starts out as a string input field, convert to int
    year = int(year)

    subset = exchange_df[
        (exchange_df['country'] == country) &
        (exchange_df['currency_name'] == currency) &
        (exchange_df['year'] == year)
    ]

    # No data was found for this combination of inputs, 
    # so user must have inputted data incorrectly or there exists no data for this year
    if subset.empty:
        return 0.0
    
    # Get the exchange rate from this DataFrame subset
    rate = subset.iloc[0]['exchange_rate']
    return rate