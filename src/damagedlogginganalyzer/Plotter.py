import matplotlib.pyplot as plt

from pathlib import Path


class Plotter:
    """
    This class provides methods to plot the wood data.
    """

    def __init__(self, out_dir):
        self.__out_dir = Path(out_dir)
        self.__x = []

    def set_x_axis(self, x):
        """
        Sets the x-axis for the plot.
        :param x:
        :return:
        """
        self.__x = x

    def preprocess_metadata(self, species, reason, origin):
        """
        Preprocesses the metadata for the plot.
        :param species:
        :param reason:
        :param origin:
        :return:
        """
        species = species.replace("/", "_")
        species = species.replace(" ", "_")
        reason = reason.replace("/", "_")
        reason = reason.replace(" ", "_")
        origin = origin.replace("/", "_")
        origin = origin.replace(" ", "_")
        return species, reason, origin

    def finish_temporal_plot(self, species, reason, origin, dir=Path()):
        """
        Finishes the temporal plot by adding labels, title, grid, saving the plot and closing it.
        :param species:
        :param reason:
        :param origin:
        :param dir:
        :return:
        """
        plt.xlabel("Jahr")
        plt.ylabel(f"Anzahl an toten {species} durch {reason} besitzt bei {origin} (1000 cbm)")
        plt.title(f"Anzahl an toten {species} durch {reason} besitzt bei {origin} über die Jahre")

        plt.grid(True)

        species, reason, origin = self.preprocess_metadata(species, reason, origin)
        directory_path = Path(f"{self.__out_dir / dir}/{species}/{reason}/{origin}")
        directory_path.mkdir(parents=True, exist_ok=True)
        file_path = directory_path / "plot.png"

        plt.savefig(file_path)
        plt.close()

    def plot_predictions(self, y, x_predict, train_score, value_2024, degree, species, reason, origin):
        """
        Plots the predictions for the damaged wood in 2024.
        :param y:
        :param x_predict:
        :param train_score:
        :param value_2024:
        :param degree:
        :param species:
        :param reason:
        :param origin:
        :return:
        """
        reason = reason.removeprefix("Einschlagsursache: ")

        species, reason, origin = self.preprocess_metadata(species, reason, origin)

        plt.figure(figsize=(10, 10))
        plt.subplot(2, 1, 1)
        plt.plot(self.__x, y, ".r", markersize=8, label="Samples")
        plt.plot(self.__x, x_predict, linewidth=5, color="tab:blue", label="Model")

        plt.text(
            2006,
            -max(y),
            f"Polynomial Regression\nBest Degree (1 is best): {degree}\nModel: Training R² Error: "
            f"{train_score:.2f}\nPrediction 2024 {value_2024}",
            fontsize=22,
            color="magenta",
        )

        self.finish_temporal_plot(species, reason, origin, Path("Prediction_2024"))

    def plot_temporal_dependencies_from_species_reason_dict(self, species_dict, species="", origin=""):
        """
        Plots the temporal dependencies for a specific species, origin and all reasons combined.
        :param species_dict:
        :param species:
        :param origin:
        :return:
        """
        plt.figure(figsize=(12, 10))

        color_map = plt.cm.get_cmap("tab10", len(species_dict))  # Use a colormap with enough colors

        for i, (key, data_points) in enumerate(species_dict.items()):
            key = key.removeprefix("Einschlagsursache: ")
            plt.plot(self.__x, data_points, label=key, color=color_map(i))

        plt.legend(title="Categories", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])

        self.finish_temporal_plot(species, "all_reasons", origin)

    def plot_temporal_dependencies_from_species_owner_dict(self, species_dict, species="", reason=""):
        """
        Plots the temporal dependencies for a specific species, reason and all owners combined.
        :param species_dict:
        :param species:
        :param reason:
        :return:
        """
        plt.figure(figsize=(18, 10))

        color_map = plt.cm.get_cmap("tab10", len(species_dict))  # Use a colormap with enough colors

        for i, (key, data_points) in enumerate(species_dict.items()):
            plt.plot(self.__x, data_points, label=key, color=color_map(i))

        plt.legend(title="Categories", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
        self.finish_temporal_plot(species, reason, "all_owners")

    def plot_temporal_dependencies(self, amounts, species="", reason="", origin=""):
        """
        Plots the temporal dependencies for a specific species, reason and origin.
        :param amounts:
        :param species:
        :param reason:
        :param origin:
        :return:
        """
        plt.figure(figsize=(14, 12))
        plt.plot(self.__x, amounts, marker="o", linestyle="-")

        reason = reason.removeprefix("Einschlagsursache: ")
        self.finish_temporal_plot(species, reason, origin)
