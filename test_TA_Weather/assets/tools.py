from sklearn.pipeline import Pipeline,FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import StandardScaler,MinMaxScaler,RobustScaler,OneHotEncoder
from sklearn.linear_model import LogisticRegression,LinearRegression
import pandas as pd
import numpy as np

class DateTransformer(TransformerMixin, BaseEstimator):
    # BaseEstimator generates get_params() and set_params() methods that all pipelines require
    # TransformerMixin creates fit_transform() method from fit() and transform()

    def __init__(self):
        pass

    def fit(self, X, y=None):
        # Store here what needs to be stored during .fit(X_train) as instance attributes.
        # Return "self" to allow chaining .fit().transform()
        return self

    def transform(self, X, y=None):
        # Return result as dataframe for integration into ColumnTransformer
        s = pd.to_datetime(X.date)
        y = s.dt.year
        m = s.dt.month
        mc = np.cos(2*np.pi*m/12)
        ms = np.sin(2*np.pi*m/12)
        cols = self.get_feature_names_out()
        return pd.DataFrame({"year":y,"monthc":mc,"months":ms,"month":m})
        

    def get_feature_names_out(self,*args):
        return ["year","monthc","months","month"]


class DeltaPressTransformer(TransformerMixin, BaseEstimator):
    # BaseEstimator generates get_params() and set_params() methods that all pipelines require
    # TransformerMixin creates fit_transform() method from fit() and transform()

    def __init__(self):
        self.regression = LinearRegression()

    def fit(self, X, y=None):
        # Store here what needs to be stored during .fit(X_train) as instance attributes.
        # Return "self" to allow chaining .fit().transform()
        self.regression.fit(X[["Altitude"]],X["pres"])
        return self

    def transform(self, X, y=None):
        # Return result as dataframe for integration into ColumnTransformer
        pres_th = self.regression.predict(X[["Altitude"]])
        return pd.DataFrame(X["pres"].values - pres_th,columns=self.get_feature_names_out())
        

    def get_feature_names_out(self,*args):
        return ["delta_pres"]