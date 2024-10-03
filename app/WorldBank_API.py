import requests
import pandas as pd
from pandas_datareader import wb
from functools import reduce


import logging
logging.basicConfig(level = logging.INFO)


class WorldBankDataAPI:
    """
    The class will fetch and save World Bank data indicators for specified countries and time periods.

    Attributes:
        country (list): A list of country codes for which data is to be fetched. Defaults to ["BR", "1W"].
        start_year (str): The starting year for the data retrieval. Defaults to "1981".
        end_year (str): The ending year for the data retrieval. Defaults to "2024".
        poverty_headcount_indicator (str): The indicator code for the poverty headcount ratio.
        individual_using_internet (str): The indicator code for individuals using the Internet.
        unemployment_total (str): The indicator code for total unemployment rate.

    Methods:
        fetch_data():
            Fetches data for the specified indicators and combines them into a single DataFrame.
            Returns a DataFrame containing the merged data for poverty, internet usage, and unemployment.

        save_to_csv(file_name="world_data.csv"):
            Saves the fetched data to a CSV file with the specified filename.
            The default filename is "world_data.csv".
    """

    def __init__(self, country=["BR", "1W"], start_year="1981", end_year="2024"):
        self.country = country
        self.start_year = start_year
        self.end_year = end_year
        self.poverty_headcount_indicator = "SI.POV.DDAY"
        self.individual_using_internet = "IT.NET.USER.ZS"
        self.unemployment_total = "SL.UEM.TOTL.ZS"
        
    def fetch_data(self):
        # Fetch data for each indicator
        df_poverty = wb.download(indicator=self.poverty_headcount_indicator, country=self.country, start=self.start_year, end=self.end_year)
        df_internet = wb.download(indicator=self.individual_using_internet, country=self.country, start=self.start_year, end=self.end_year)
        df_unemployment = wb.download(indicator=self.unemployment_total, country=self.country, start=self.start_year, end=self.end_year)
        
        # Combine the dataframes
        dfs = [df_poverty, df_internet, df_unemployment]
        final_df = reduce(lambda left, right: pd.merge(left, right, on=['country', 'year'], how='outer'), dfs).fillna("-")
        
        # Rename the columns
        header_rename = {
            'SI.POV.DDAY': 'Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)', 
            'IT.NET.USER.ZS': 'Individuals using the Internet (% of population)', 
            'SL.UEM.TOTL.ZS': 'Unemployment, total (% of total labor force) (modeled ILO estimate)'
        }
        final_df.rename(columns=header_rename, inplace=True)
        
        return final_df
    
    def save_to_csv(self, file_name="world_data.csv"):
        final_df = self.fetch_data()
        final_df.to_csv(file_name, index=True)
        logging.info(f"Data saved to {file_name}\n")
