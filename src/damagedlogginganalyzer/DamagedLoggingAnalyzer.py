from damagedlogginganalyzer.CSVAnalyzer import CSVAnalyzer


class DamagedLoggingAnalyzer(CSVAnalyzer):
    def __init__(self):
        super().__init__()

    def analyze(self):
        '''
        Solves the question in the README.md
        :return:
        '''
        year_dict = self.get_dict_with_df_same_key_value('Jahr')
        print(year_dict['2006'])
