import pandas as pd

from pathlib import Path


class CSVAnalyzer:
    """
    This class reads in a CSV file and provides methods to preprocess the csv data.
    """

    def __init__(self):
        self.__csv = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def read_in_csv(self, csv_file):
        """
        Read in a CSV file and saves it into self.__csv.
        :param csv_file:
        :return:
        """
        csv = Path(csv_file)
        if not csv.exists():
            raise FileExistsError(f"{csv} does not exists!. Please enter correct Path to your CSV file!")

        self.__csv = pd.read_csv(csv)

    def get_dict_with_df_same_key_value(self, key=''):
        """
        Returns a dictionary, which contains all rows of the csv with the same key value as data frame.
        :param key:
        :return:
        """
        try:
            unique_key_values = self.__csv[key].unique()
            unique_key_values = list(filter(lambda x: x not in ['__________'], unique_key_values))
        except KeyError:
            raise KeyError(
                f'Your CSV does not contain a column with value: {key}! Possible values are {self.__csv.keys()}')

        # Create a dictionary to store DataFrames for each key value
        values_dataframes = {}

        for value in unique_key_values:
            value_df = self.__csv[self.__csv[key] == value]
            values_dataframes[value] = value_df

        return values_dataframes
