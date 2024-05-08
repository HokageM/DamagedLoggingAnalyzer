import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold

from damagedlogginganalyzer.CSVAnalyzer import CSVAnalyzer
from damagedlogginganalyzer.Plotter import Plotter


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
        self.__plotter = Plotter(out_dir)

        self.__ksplits = 9

    def __exit__(self, exc_type, exc_val, exc_tb):
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
        self.__plotter.set_x_axis(self.__years)
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
                self.__plotter.plot_temporal_dependencies(amounts[specie][reason], specie, reason, "Insgesamt")
            # Create Combined Plots
            self.__plotter.plot_temporal_dependencies_from_species_dict(amounts[specie], specie, "Insgesamt")

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

                value_2024 = model.predict(poly_features.transform([[2024]]))
                print(f"{specie}, {reason}, Insgesamt in 2024:", value_2024)

                self.__plotter.plot_predictions(x_poly, y, model.predict(x_poly), train_score, value_2024, degree, specie,
                                                reason, "Insgesamt")
