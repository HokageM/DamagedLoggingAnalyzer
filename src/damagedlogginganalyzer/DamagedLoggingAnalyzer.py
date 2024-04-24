import pandas as pd

from pathlib import Path


class DamagedLoggingAnalyzer:
    def __init__(self):
        self.__csv = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def read_in_csv(self, csv_file):
        '''
        Read in a CSV file and saves it into self.__csv.
        :param csv_file:
        :return:
        '''
        csv = Path(csv_file)
        if not csv.exists():
            raise FileExistsError(f"{csv} does not exists!. Please enter correct Path to your CSV file!")

        self.__csv = pd.read_csv(csv)

    def analyze(self):
        # Display the DataFrame
        print(self.__csv[9:])  # The first rows are meta data.f
        data_df = self.__csv
        print(data_df.keys())
        print(data_df['Jahr'])

        # finde indices of all rows that are from 2006
        # indices = df[df['Year'] == 2006].index
        # print(indices)
        # print(df[df['Year'] == 2006])
