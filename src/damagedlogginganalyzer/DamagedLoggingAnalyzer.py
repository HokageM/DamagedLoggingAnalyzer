import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

from damagedlogginganalyzer.CSVAnalyzer import CSVAnalyzer


class DamagedLoggingAnalyzer(CSVAnalyzer):
    """
    This class provides methods to analyze the data about damaged wood from the CSV file.
    """

    def __init__(self, out_dir="plots"):
        super().__init__()
        self.__year_dict = {}
        self.__years = None

        self.__out_dir = out_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        plt.close("all")
        super().__exit__(exc_type, exc_val, exc_tb)

    def analyze_temporal_dependencies(self):
        """
        Analyzes the temporal dependencies of the data.
        :return:
        """
        species = self.__year_dict[2020]["Baumart"].unique()
        reasons = self.__year_dict[2020].filter(like="Einschlagsursache:").columns
        amounts = {}
        for specie in species:
            amounts[specie] = {}
            for reason in reasons:
                # Create Single Plots
                amounts[specie][reason] = self.collect_temporal_dependencies(specie, reason, "Insgesamt")
                self.plot_temporal_dependencies(amounts[specie][reason], specie, reason, "Insgesamt")
            # Create Combined Plots
            self.plot_temporal_dependencies_from_species_dict(amounts[specie], specie, "Insgesamt")

    def collect_temporal_dependencies(self, species="", reason="", origin=""):
        """
        Collects the temporal dependencies for a specific species, reason and origin.
        :param species:
        :param reason:
        :param origin:
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

    def plot_temporal_dependencies_from_species_dict(self, species_dict, species="", origin=""):
        """
        Plots the temporal dependencies for a specific species and origin.
        :param species_dict:
        :param species:
        :param origin:
        :return:
        """
        plt.figure(figsize=(12, 10))

        color_map = plt.cm.get_cmap("tab10", len(species_dict))  # Use a colormap with enough colors

        # Iterate over each key-value pair in the dictionary
        for i, (key, data_points) in enumerate(species_dict.items()):
            key = key.removeprefix("Einschlagsursache: ")
            plt.plot(self.__years, data_points, label=key, color=color_map(i))

        plt.xlabel("Jahr")
        plt.ylabel(f"Anzahl an toten {species} (1000 cbm)")
        plt.title(f"Anzahl an toten {species} über die Jahre")

        plt.legend(title="Categories", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.tight_layout()

        species = species.replace("/", "_")
        species = species.replace(" ", "_")
        origin = origin.replace("/", "_")
        origin = origin.replace(" ", "_")
        directory_path = Path(f"{self.__out_dir}/{species}/all_reasons/{origin}")
        directory_path.mkdir(parents=True, exist_ok=True)
        file_path = directory_path / "plot.png"

        plt.savefig(file_path)
        plt.close()

    def plot_temporal_dependencies(self, amounts, species="", reason="", origin=""):
        """
        Plots the temporal dependencies for a specific species, reason and origin.
        :param amounts:
        :param species:
        :param reason:
        :param origin:
        :return:
        """
        plt.figure(figsize=(12, 10))
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
        directory_path = Path(f"{self.__out_dir}/{species}/{reason}/{origin}")
        directory_path.mkdir(parents=True, exist_ok=True)
        file_path = directory_path / "plot.png"
        plt.savefig(file_path)
        plt.close()

    def analyze(self, temporal_dependencies=True):
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

        if temporal_dependencies:
            # Analyze different aspects
            self.analyze_temporal_dependencies()
