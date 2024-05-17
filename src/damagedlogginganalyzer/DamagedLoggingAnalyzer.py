import numpy as np

from damagedlogginganalyzer.CSVAnalyzer import CSVAnalyzer
from damagedlogginganalyzer.Plotter import Plotter
from damagedlogginganalyzer.WoodOracle import WoodOracle


class DamagedLoggingAnalyzer(CSVAnalyzer):
    """
    This class provides methods to analyze the data about damaged wood from the CSV file.
    """

    def __init__(self, out_dir="plots"):
        super().__init__()
        self.__year_dict = {}
        self.__species = []
        self.__reasons = []
        self.__owners = []
        self.__years = []

        self.__out_dir = out_dir
        self.__plotter = Plotter(out_dir)

        self.__wood_oracle = WoodOracle()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)

    def analyze(
        self,
        *,
        plot_reason_dependencies=False,
        plot_owner_dependencies=False,
        plot_temporal_dependencies_all=False,
        predict_temporal_dependencies=False,
        calculate_most_dangerous_reasons=False,
    ):
        """
        Solves the question in the README.md
        :return:
        """
        self.__year_dict = self.get_dict_with_df_same_key_value("Jahr")
        self.__species = self.__year_dict[2020]["Baumart"].unique()
        self.__reasons = self.__year_dict[2020].filter(like="Einschlagsursache:").columns
        self.__owners = self.__year_dict[2020]["Waldeigentum"].unique()
        self.__years = np.zeros(self.__year_dict.keys().__len__())
        idx = 0
        for year in self.__year_dict:
            self.__years[idx] = year
            idx += 1
        self.__plotter.set_x_axis(self.__years)
        if plot_temporal_dependencies_all:
            print("Plotting Temporal Dependencies (all specie, reason and owner combinations)...")
            self.temporal_plot_all_combinations()
            print(f"Plots saved in: {self.__out_dir}")
        if plot_reason_dependencies:
            print("Plotting Reason Dependencies ...")
            self.reason_dependencies_plot()
            print(f"Plots saved in: {self.__out_dir}")
        if plot_owner_dependencies:
            print("Plotting Owner Dependencies ...")
            self.owner_dependencies_plot()
            print(f"Plots saved in: {self.__out_dir}")
        if predict_temporal_dependencies:
            # Predict the amount of damaged wood in 2024
            self.predict_temporal_dependencies()
        if calculate_most_dangerous_reasons:
            self.calculate_most_dangerous_reasons()

    def calculate_most_dangerous_reasons(self):
        """
        Calculates the most dangerous reasons for each specie.
        :return:
        """
        total_amounts = {}
        for specie in self.__species:
            amounts = {}
            for reason in self.__reasons:
                if reason not in total_amounts:
                    total_amounts[reason] = 0
                amounts[reason] = self.collect_temporal_dependencies(specie, reason, "Insgesamt").sum()
                total_amounts[reason] += amounts[reason]

            print(f"Most dangerous reasons for {specie}:")
            sorted_amounts = sorted(amounts.items(), key=lambda x: x[1], reverse=True)
            for reason, value in sorted_amounts:
                print(f"{reason}: {value}")

    def temporal_plot_all_combinations(self):
        """
        Plots all temporal dependencies for each specie, reason and owner.
        :return:
        """
        for specie in self.__species:
            for reason in self.__reasons:
                for owner in self.__owners:
                    amounts = self.collect_temporal_dependencies(specie, reason, owner)
                    self.__plotter.plot_temporal_dependencies(amounts, specie, reason, owner)

    def owner_dependencies_plot(self):
        """
        Plots all temporal dependencies for each specie and reason for all owners.
        :return:
        """
        amounts = {}
        for specie in self.__species:
            amounts[specie] = {}
            for reason in self.__reasons:
                for owner in self.__owners:
                    amounts[specie][owner] = self.collect_temporal_dependencies(specie, reason, owner)
                reason = reason.removeprefix("Einschlagsursache: ")
                self.__plotter.plot_temporal_dependencies_from_species_owner_dict(amounts[specie], specie, reason)

    def reason_dependencies_plot(self):
        """
        Plots all temporal dependencies for each specie and owner for all reasons.
        :return:
        """
        amounts = {}
        for specie in self.__species:
            amounts[specie] = {}
            for owner in self.__owners:
                for reason in self.__reasons:
                    amounts[specie][reason] = self.collect_temporal_dependencies(specie, reason, owner)
                self.__plotter.plot_temporal_dependencies_from_species_reason_dict(amounts[specie], specie, owner)

    def collect_temporal_dependencies(self, species="", reason="", origin=""):
        """
        Collects the temporal dependencies for a specific species, reason and origin.
        :param species: Species of the tree
        :param reason: Reason for the damaged wood
        :param origin: Origin/ owner of the tree
        :return:
        """
        amounts = np.zeros(self.__year_dict.keys().__len__())

        idx = 0
        for year in self.__year_dict:
            all_species_in_year = self.__year_dict[year][self.__year_dict[year]["Baumart"] == species]
            all_orig_all_spec_in_year = all_species_in_year[all_species_in_year["Waldeigentum"] == origin]
            amounts[idx] = all_orig_all_spec_in_year[reason].iloc[0]
            idx += 1
        return amounts

    def predict_temporal_dependencies(self):
        """
        Predicts the amount of damaged wood in 2024. And plots the predicted function.
        :return:
        """
        x = self.__years.reshape(-1, 1)

        amounts = {}
        for specie in self.__species:
            amounts[specie] = {}
            for reason in self.__reasons:
                for owner in self.__owners:
                    y = self.collect_temporal_dependencies(specie, reason, owner)
                    train_predict, train_score, value_2024, degree = self.__wood_oracle.predict_wood_logging(
                        x, y, specie, reason, owner
                    )

                    self.__plotter.plot_predictions(
                        y, train_predict, train_score, value_2024, degree, specie, reason, owner
                    )
