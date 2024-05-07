import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold

from damagedlogginganalyzer.CSVAnalyzer import CSVAnalyzer


class DamagedLoggingAnalyzer(CSVAnalyzer):
    """
    This class provides methods to analyze the data about damaged wood from the CSV file.
    """

    def __init__(self, out_dir="plots"):
        super().__init__()
        self.__year_dict = {}
        self.__species = []
        self.__reasons = []
        self.__years = []

        self.__out_dir = out_dir

        self.__ksplits = 9

    def __exit__(self, exc_type, exc_val, exc_tb):
        plt.close("all")
        super().__exit__(exc_type, exc_val, exc_tb)

    def analyze(self, plot_temporal_dependencies=False, predict=False):
        """
        Solves the question in the README.md
        :return:
        """
        self.__year_dict = self.get_dict_with_df_same_key_value("Jahr")
        self.__species = self.__year_dict[2020]["Baumart"].unique()
        self.__reasons = self.__year_dict[2020].filter(like="Einschlagsursache:").columns
        self.__years = np.zeros(self.__year_dict.keys().__len__())
        idx = 0
        for year in self.__year_dict:
            self.__years[idx] = year
            idx += 1

        if plot_temporal_dependencies:
            self.plot_all_temporal_combinations()

        if predict:
            # Predict the amount of damaged wood in 2024
            self.predict_temporal_dependencies()

    def plot_all_temporal_combinations(self):
        """
        Plots all temporal dependencies for each species and reason.
        :return:
        """
        amounts = {}
        for specie in self.__species:
            amounts[specie] = {}
            for reason in self.__reasons:
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

    def polynomial_regression(self, x_train, y_train, x_test, y_test, degree):
        """
        Trains a polynomial regression model with the given degree.
        :param x_train:
        :param y_train:
        :param x_test:
        :param y_test:
        :param degree:
        :return:
        """
        poly_features = PolynomialFeatures(degree=degree)
        x_train_poly = poly_features.fit_transform(x_train)
        x_test_poly = poly_features.transform(x_test) if len(y_test) > 0 else None

        model = LinearRegression()
        model.fit(x_train_poly, y_train)

        train_score = model.score(x_train_poly, y_train)
        test_score = model.score(x_test_poly, y_test) if len(y_test) > 0 else None

        return model, train_score, test_score

    def k_fold_cross_validation(self, x, y):
        """
        Performs k-fold cross validation to find the best degree for the polynomial regression model.
        :param x:
        :param y:
        :return:
        """
        degrees = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        kf = KFold(n_splits=self.__ksplits, shuffle=True, random_state=0)
        a_train_errors = []
        a_test_errors = []
        for degree in degrees:
            train_scores = []
            test_scores = []
            for train_index, val_index in kf.split(x):
                x_train, x_test = x[train_index], x[val_index]
                y_train, y_test = y[train_index], y[val_index]

                model, train_score, test_score = self.polynomial_regression(x_train, y_train, x_test, y_test, degree)

                train_scores.append(train_score)
                test_scores.append(test_score)

            # Calculate average training and validation scores
            avg_train_score = np.abs(np.mean(train_scores))
            avg_val_score = np.abs(np.mean(test_scores))

            a_train_errors.append(avg_train_score)
            a_test_errors.append(avg_val_score)

        minimum_value = np.min(a_test_errors)
        best_degree = degrees[a_test_errors.index(minimum_value)]
        print(f"Minimum value: {minimum_value} at index {a_test_errors.index(minimum_value)}")
        print(f"Best degree: {best_degree}")

        best_model, train_score, _ = self.polynomial_regression(x, y, [], [], best_degree)
        print(f"Train R² score (1 is best) for the best model: {train_score}")
        return best_model, best_degree, train_score

    def predict_temporal_dependencies(self):
        x = self.__years.reshape(-1, 1)

        amounts = {}
        for specie in self.__species:
            amounts[specie] = {}
            for reason in self.__reasons:
                y = self.collect_temporal_dependencies(specie, reason, "Insgesamt")

                model, degree, train_score = self.k_fold_cross_validation(x, y)

                poly_features = PolynomialFeatures(degree=degree)
                x_poly = poly_features.fit_transform(x)

                value = model.predict(poly_features.transform([[2024]]))
                print(f"{specie}, {reason}, Insgesamt in 2024:", value)

                # Save the plot as an image file
                specie_mod = specie.replace("/", "_")
                specie_mod = specie_mod.replace(" ", "_")
                reason_mod = reason.removeprefix("Einschlagsursache: ")
                reason_mod = reason_mod.replace("/", "_")
                reason_mod = reason_mod.replace(" ", "_")

                directory_path = Path(f"{self.__out_dir}/Prediction_2024/{specie_mod}/{reason_mod}/Insgesamt")
                directory_path.mkdir(parents=True, exist_ok=True)
                file_path = directory_path / "polynomial_reg_plot.png"

                plt.figure(figsize=(10, 10))
                plt.subplot(2, 1, 1)
                plt.plot(x, y, ".r", markersize=8, label="Samples")
                plt.plot(x, model.predict(x_poly), linewidth=5, color="tab:blue", label="Model")

                plt.xlabel("Jahr")
                plt.ylabel(f"Anzahl an toten {specie} durch {reason_mod} (1000 cbm)")
                plt.title(f"Polynomial Regression ({degree}) for {specie} because of {reason_mod}")
                plt.text(
                    2006,
                    -max(y),
                    f"Best Degree (1 is best): {degree}\nModel: Training R² Error: "
                    f"{train_score:.2f}\nPrediction 2024 {value}",
                    fontsize=22,
                    color="magenta",
                )
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
