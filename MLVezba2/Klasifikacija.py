
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from sklearn import clone
from sklearn.datasets import fetch_openml
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_val_predict

print("pocetak")
mnist = fetch_openml('mnist_784', version=1)
print("1")
#mnist.keys()
print("2")

#dataset 28x28 piksela brojeva

X, y = mnist["data"], mnist["target"]

some_digit = X.iloc[0]
some_digit_image = some_digit.values.reshape(28, 28)

plt.imshow(some_digit_image, cmap="binary")
plt.axis("off")
plt.show()

y = y.astype(np.uint8) #pretvaramo stringove u brojeve

X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]

y_train_5 = (y_train == 5) #pravimo vektor koji nam govori koje su sve petice
y_test_5 = (y_test == 5)

sgd_clf = SGDClassifier(random_state=42)
sgd_clf.fit(X_train, y_train_5)

print(sgd_clf.predict([some_digit]))

# Implementacija cross validacije

skfolds = StratifiedKFold(n_splits=3)

#for train_index, test_index in skfolds.split(X_train, y_train_5):
#    clone_clf = clone(sgd_clf)
#    X_train_folds = X_train[train_index]
#    y_train_folds = y_train_5[train_index]
#    X_test_fold = X_train[test_index]
#    y_test_fold = y_train_5[train_index]

#    clone_clf.fit(X_train_folds,y_train_folds)
#    y_pred = clone_clf.predict(X_test_fold)
#    n_correct = sum(y_pred == y_test_fold)
#    print(n_correct/len(y_pred))

print(cross_val_score(sgd_clf, X_train, y_train_5, cv=3, scoring="accuracy"))

y_train_pred = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3)

confusion_matrix(y_train_5, y_train_pred)



