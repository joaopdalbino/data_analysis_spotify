from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd
from os.path import dirname, abspath
from statsmodels.tools.eval_measures import rmse

path = dirname(dirname(abspath(__file__)))

df = pd.read_csv(path + '/results/data/spotify_numerical_features_only.csv')

polynomial_features = PolynomialFeatures(degree=4)

X = polynomial_features.fit_transform(df.drop(columns = ['popularity'], axis=1))

X_predict = pd.read_csv(path + '/results/data/4 - spotify_numerical_features_only - predict.csv')

model = LinearRegression()
model.fit(X, df['popularity'])

y_poly_pred = model.predict(X)

df['y predict'] = y_poly_pred

print(rmse(df['popularity'], df['y predict']))

#X_predict.to_csv(path+'/results/linear regression/data/4 - final_result - polynomial_features.csv',index=False)