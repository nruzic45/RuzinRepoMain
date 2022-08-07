from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from data_normalize import normalize_data,class_weights
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.metrics import f1_score

x,y = normalize_data("Train-dataset.csv",include=['WELL','X_Y','DEPOSITIONAL_ENVIRONMENT'],hot_one_enc=False)
weights = class_weights("Train-dataset.csv")
x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(x, y, test_size = 0.15,stratify=y)

model = RandomForestClassifier(n_estimators=100, class_weight=weights)
model.fit(x_training_data,y_training_data)
prediction=model.predict(x_test_data)

print("The prediction accuracy is: ",model.score(x_test_data,y_test_data)*100,"%")

cm = confusion_matrix(y_test_data, prediction)
print(cm)

sn.heatmap(cm, annot=True, fmt='g')
plt.show()

print(f1_score(y_test_data, prediction,average='micro'))