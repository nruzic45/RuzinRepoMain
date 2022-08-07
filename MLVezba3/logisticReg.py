import numpy as np
from matplotlib import pyplot as plt
from sklearn import datasets
from sklearn.linear_model import LogisticRegression

iris = datasets.load_iris()
X = iris["data"][:, 3:]
y = (iris["target"] == 2).astype(int)

log_reg = LogisticRegression()
log_reg.fit(X, y)

X_new = np.linspace(0, 3, 1000).reshape(-1, 1)
y_proba = log_reg.predict_proba(X_new)
plt.plot(X_new, y_proba[:, 1], "g-", label="Iris virginica")
plt.plot(X_new, y_proba[:, 0], "g-", label="Not Iris virginica")
plt.show()

X = iris["data"][:, (2, 3)]
y = iris["target"]

softmax_reg = LogisticRegression(multi_class="multinomial", solver= "lbfgs", C=10)
softmax_reg.fit(X, y)
print(softmax_reg.predict_proba([[5,2]])) #moze da izbaci i probability(tj povrsinu logisticke krive do unetih vrednosti(za 1d sluc))

