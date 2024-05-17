import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold


class Oracle:
    """
    This class provides methods to perform k-fold cross validation to find the best degree for the polynomial regression
    """

    def __init__(self):
        self.k_splits = 9

    def k_fold_cross_validation(self, x, y):
        """
        Performs k-fold cross validation to find the best degree for the polynomial regression model.
        :param x:
        :param y:
        :return:
        """
        degrees = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

        kf = KFold(n_splits=self.k_splits, shuffle=True, random_state=0)
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
        print(f"Train R² score (1 is best) for the best model: {train_score}\n")
        return best_model, best_degree, train_score

    @staticmethod
    def polynomial_regression(x_train, y_train, x_test, y_test, degree):
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
