from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split

from data_normalize import normalize_data
from statistic import statistika, confusion_matrix_show

x, y = normalize_data("Train-dataset.csv", include=['WELL' ,'X_Y', 'DEPOSITIONAL_ENVIRONMENT'], hot_one_enc=False)
x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(x, y, test_size=0.15, stratify=y,random_state=0)


clf = ExtraTreesClassifier(n_estimators=1000, random_state=0,n_jobs=-1)
clf.fit(x_training_data, y_training_data)

print(clf.score(x_training_data, y_training_data))
print(clf.score(x_test_data,y_test_data))

prediction_rf_training = clf.predict(x_training_data)
prediction_rf_test = clf.predict(x_test_data)

print("Training RandomForest: \n")
statistika(prediction_rf_training, y_training_data)
confusion_matrix_show(prediction_rf_training,y_training_data)
print("*********************\n")
print("Test RandomForest: \n")
s = statistika(prediction_rf_test, y_test_data)
confusion_matrix_show(prediction_rf_test, y_test_data)