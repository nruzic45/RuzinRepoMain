from sklearn.metrics import f1_score, accuracy_score, precision_score, classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sn
from matplotlib import pyplot as plt


def statistika(prediction, y_data):
    print("The prediction accuracy is: ", accuracy_score(y_data, prediction) * 100, "%")
    print("The prediction f1 score is: ", f1_score(y_data, prediction, average='weighted')*100, "%")
    print("The prediction precision is: ", precision_score(y_data, prediction, average='weighted') * 100, "%")
    print(classification_report(y_data, prediction, zero_division=0))
    return f1_score(y_data, prediction, average='weighted')*100

def confusion_matrix_show(prediction, y_data):
    cm = confusion_matrix(y_data, prediction)
    #print(cm)
    sn.heatmap(cm, annot=True, fmt='g')
    plt.show()

