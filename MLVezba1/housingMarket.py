import tarfile

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit, cross_val_score, GridSearchCV
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.tree import DecisionTreeRegressor

housing_tgz = tarfile.open("housing.tgz")
housing_tgz.extractall(path="C:/Users/Nikola/Documents/GitHub/Repo1/")
housing_tgz.close()

data = pd.read_csv("C:/Users/Nikola/Documents/GitHub/Repo1/housing.csv")
print(data.head())

#print(data["ocean_proximity"].value_counts())

print(data.describe())



#data.hist(bins=50, figsize=(20,15))
#plt.show()

#train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)

data["income_cat"] = pd.cut(data["median_income"], bins=[0.,1.5,3.0,4.5,6.,np.inf], labels=[1, 2, 3, 4, 5])
data["income_cat"].hist()
#plt.show()

split = StratifiedShuffleSplit(n_splits=1, test_size = 0.2, random_state = 42)
for train_index, test_index in split.split(data, data["income_cat"]):
    strat_train_set = data.loc[train_index]
    strat_test_set = data.loc[test_index]

test = strat_test_set["income_cat"].value_counts()/len(strat_test_set)
#print(test)


for set_ in (strat_train_set, strat_test_set):
    set_.drop("income_cat", axis = 1, inplace=True)

housing = strat_train_set.copy()
housing_labels = strat_train_set["median_house_value"].copy()


housing.plot(kind = "scatter", x="longitude", y="latitude", alpha = 0.4,
             s=housing["population"]/100, label = "population", figsize = (10,7),
             c="median_house_value",cmap = plt.get_cmap("jet"), colorbar = True, )
plt.legend()
plt.show()

corr_matrix = housing.corr()
print("corr mat")
print(corr_matrix)
print(corr_matrix["median_house_value"].sort_values(ascending=False))

#ciscenje podataka

imputer = SimpleImputer(strategy = "median")

housing_num = housing.drop("ocean_proximity", axis=1) #drop the nonnumerical columns
imputer.fit(housing_num)
print(imputer.statistics_)

X = imputer.transform(housing_num)

housing_tr = pd.DataFrame(X, columns=housing_num.columns,
                          index = housing_num.index)
#estimatori, transformator, prediktor
#.strategy vraca hyperparametre, statistics_ vraca parametre(donja cvrta u sufiksu)


housing_cat = housing[["ocean_proximity"]]
print(housing_cat.head(10))

#kodiranje kategorickih vrednosti prirodnim brojevima od 0 do N
ordinal_encoder = OrdinalEncoder()
housing_cat_encoded = ordinal_encoder.fit_transform(housing_cat)
#print(housing_cat_encoded[:10])
#print(ordinal_encoder.categories_)

#enkoder sa binarnim vrednostima 1HOT

cat_encoder = OneHotEncoder()
housing_cat_1hot = cat_encoder.fit_transform(housing_cat)
#print(housing_cat_1hot)



# Definisanje svoje sopstvene transform klase
rooms_ix, bedrooms_ix, population_ix, household_ix = 3, 4, 5, 6

class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room = True):
        self.add_bedrooms_per_room = add_bedrooms_per_room
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        rooms_per_household = X[:, rooms_ix]/ X[:, household_ix]
        population_per_household = X[:, population_ix]/ X[:, household_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix]/X[:, rooms_ix]
            return np.c_[X, rooms_per_household,population_per_household,bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household,population_per_household]

attr_adder = CombinedAttributesAdder(add_bedrooms_per_room = False)
housing_extra_attribs = attr_adder.transform(housing.values)

#skaliranje
#BITNO

#min max i standardization
#min max oduzmemo minimalnu vrednost transliramo podatke ka 0 i podelimo sa razlikom max - min
#standar. oduzmemo srednju vrednost i odelimo sa standardnom devijacijom
#SKALRIATI JEDINO TRAINING DATA
#!
#!
#!


#PIPELINES
#poziva fit_transform redom do posledenjeg tranfsormatora , tu poziva fit, transform ili fit transform
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy="median")),
     ('attribs_adder', CombinedAttributesAdder()),
     ('std_scaler', StandardScaler()),
])

housing_num_tr = num_pipeline.fit_transform(housing_num)

#pipeline za tranformaciju kolona
#trazi listu transformatora, u foramtu ("ime", transformator, imeKolona)
num_attribs = list(housing_num)
cat_atribs = ["ocean_proximity"]

full_pipeline = ColumnTransformer([
    ("num", num_pipeline, num_attribs),
    ("cat", OneHotEncoder(), cat_atribs),
])

housing_prepared = full_pipeline.fit_transform(housing)



############################################### Faza 2
#Gotova preparacija podataka vreme je za Modeliranje

lin_reg = LinearRegression()
print("\n\n\n")
lin_reg.fit(housing_prepared, housing_labels)

housing_predictions = lin_reg.predict(housing_prepared)
lin_mse = mean_squared_error(housing_labels, housing_predictions)
lin_rmse = np.sqrt(lin_mse)

#print(lin_rmse)

tree_reg = DecisionTreeRegressor()
tree_reg.fit(housing_prepared, housing_labels)

housing_predictions = tree_reg.predict(housing_prepared)
lin_mse = mean_squared_error(housing_labels, housing_predictions)
lin_rmse = np.sqrt(lin_mse)

#print(lin_rmse)

scores = cross_val_score(tree_reg, housing_prepared, housing_labels,
                         scoring="neg_mean_squared_error",cv = 10)
tree_rmse_scores = np.sqrt(-scores)

#print(tree_rmse_scores)
#print(tree_rmse_scores.mean())
#print(tree_rmse_scores.std())


#oprimizacija hiper parametara
#grid search

param_grid = [
    {'n_estimators': [3,10,30], 'max_features': [2,4,6,8]},
    {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2,3,4]}
]

forest_reg = RandomForestRegressor()

grid_search = GridSearchCV(forest_reg, param_grid, cv = 5,
                           scoring='neg_mean_squared_error',
                           return_train_score = True)

grid_search.fit(housing_prepared, housing_labels)

final_model = grid_search.best_estimator_

X_test = strat_test_set.drop("median_house_value", axis=1)
y_test = strat_test_set["median_house_value"].copy()

X_test_prepared = full_pipeline.transform(X_test)

final_predictions = final_model.predict(X_test_prepared)

final_mse = mean_squared_error(y_test, final_predictions)
final_rmse = np.sqrt(final_mse)

print("\n\n\n")
print(final_rmse)
