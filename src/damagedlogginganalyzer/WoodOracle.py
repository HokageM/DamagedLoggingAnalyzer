from sklearn.preprocessing import PolynomialFeatures

from damagedlogginganalyzer.Oracle import Oracle


class WoodOracle(Oracle):
    """
    This class provides methods to predict the amount of damaged wood in 2024.
    """

    def __init__(self):
        super().__init__()

    def predict_wood_logging(self, x, y, species, reason, origin):
        """
        Predicts the amount of damaged wood in 2024.
        :param x: Input data
        :param y: Output data
        :param species: Species of the tree
        :param reason: Reason for the damage
        :param origin: Origin/ owner of the tree
        :return:
        """
        model, degree, train_score = self.k_fold_cross_validation(x, y)

        poly_features = PolynomialFeatures(degree=degree)
        x_poly = poly_features.fit_transform(x)

        value_2024 = model.predict(poly_features.transform([[2024]]))
        print(f"{species}, {reason}, {origin} in 2024:", value_2024)

        return model.predict(x_poly), train_score, value_2024, degree
