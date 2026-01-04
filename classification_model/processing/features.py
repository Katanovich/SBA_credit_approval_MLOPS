from sklearn.base import BaseEstimator, TransformerMixin


class ExtractLetterTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, variables):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):


        X = X.copy()

        for feature in self.variables:
            X[feature] = X[feature].str[0]

        return X
