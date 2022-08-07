from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import seaborn as sn
from data_normalize import normalize_data

x, y = normalize_data("Train-dataset.csv", include=['WELL', 'X_Y', 'DEPOSITIONAL_ENVIRONMENT'], hot_one_enc=False)
x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(x, y, test_size=0.15,stratify=y)

model = SVC(kernel='poly')
model.fit(x_training_data, y_training_data)

prediction = model.predict(x_test_data)

print("The prediction accuracy is: ", model.score(x_test_data, y_test_data) * 100, "%")

cm = confusion_matrix(y_test_data, prediction)
print(cm)

sn.heatmap(cm, annot=True, fmt='g')
plt.show()

print(f1_score(y_test_data, prediction,average='micro'))