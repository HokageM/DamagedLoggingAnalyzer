import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

from damagedlogginganalyzer.CSVAnalyzer import CSVAnalyzer


class DamagedLoggingAnalyzer(CSVAnalyzer):
    def __init__(self):
        super().__init__()
        self.__year_dict = {}
        self.__years = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        plt.close("all")
        super().__exit__(exc_type, exc_val, exc_tb)

    def analyze_temporal_dependencies(
        self,
        species="Eiche und Roteiche",
        reason="Einschlagsursache: Wind/ Sturm",
        origin="Insgesamt",
    ):
        amounts = np.zeros(self.__year_dict.keys().__len__())

        idx = 0
        for year in self.__year_dict:
            all_species_in_year = self.__year_dict[year][
                self.__year_dict[year]["Baumart"] == species
            ]
            all_orig_all_spec_in_year = all_species_in_year[
                all_species_in_year["Waldeigentum"] == origin
            ]
            amounts[idx] = all_orig_all_spec_in_year[reason].iloc[0]
            idx += 1
        self.plot_temporal_dependencies(amounts, species, reason, origin)

    def plot_temporal_dependencies(
        self,
        amounts,
        species="Eiche und Roteiche",
        reason="Einschlagsursache: Wind/ Sturm",
        origin="Insgesamt",
    ):
        plt.plot(self.__years, amounts, marker="o", linestyle="-")

        # Adding labels and title
        plt.xlabel("Jahr")
        reason = reason.removeprefix("Einschlagsursache: ")
        plt.ylabel(f"Anzahl an toten {species} durch {reason} (1000 cbm)")
        plt.title(f"Anzahl an toten {species} durch {reason} über die Jahre")

        # Display the plot
        plt.grid(True)

        # Save the plot as an image file
        species = species.replace("/", "_")
        species = species.replace(" ", "_")
        reason = reason.replace("/", "_")
        reason = reason.replace(" ", "_")
        origin = origin.replace("/", "_")
        origin = origin.replace(" ", "_")
        directory_path = Path(f"plots/{species}/{reason}/{origin}")
        directory_path.mkdir(parents=True, exist_ok=True)
        file_path = directory_path / "plot.png"
        plt.savefig(file_path)

        plt.show()

    def analyze(self):
        """
        Solves the question in the README.md
        :return:
        """
        self.__year_dict = self.get_dict_with_df_same_key_value("Jahr")

        self.__years = np.zeros(self.__year_dict.keys().__len__())
        idx = 0
        for year in self.__year_dict:
            self.__years[idx] = year
            idx += 1

        # Analyze different aspects
        self.analyze_temporal_dependencies()
