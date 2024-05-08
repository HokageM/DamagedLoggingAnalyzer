import matplotlib.pyplot as plt

from pathlib import Path

class Plotter:
    """
    This class provides methods to plot the wood data.
    """

    def __init__(self, out_dir):
        self.__out_dir = out_dir
        self.__x = []

    def set_x_axis(self, x):
        """
        Sets the x-axis for the plot.
        :param x:
        :return:
        """
        self.__x = x

    def finish_temporal_plot(self, species, reason, origin):
        """
        Finishes the temporal plot by adding labels, title, grid, saving the plot and closing it.
        :param species:
        :param reason:
        :param origin:
        :return:
        """
        plt.xlabel("Jahr")
        plt.ylabel(f"Anzahl an toten {species} durch {reason} (1000 cbm)")
        plt.title(f"Anzahl an toten {species} durch {reason} über die Jahre")

        plt.grid(True)
        plt.tight_layout()

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
            plt.plot(self.__x, data_points, label=key, color=color_map(i))

        self.finish_temporal_plot(species, "all_reasons", origin)

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
        plt.plot(self.__x, amounts, marker="o", linestyle="-")

        reason = reason.removeprefix("Einschlagsursache: ")
        self.finish_temporal_plot(species, reason, origin)
