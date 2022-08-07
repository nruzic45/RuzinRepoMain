import numpy as np
from sklearn import datasets
from sklearn.datasets import make_moons
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.svm import LinearSVC, SVC, LinearSVR, SVR

iris = datasets.load_iris()
X = iris["data"][:, (2, 3)]
y = (iris["target"] == 2).astype(np.float64)


svm_clf = Pipeline([
    ("scaler", StandardScaler()),
    ("linear_svc", LinearSVC(C=1, loss="hinge")),

])
svm_clf.fit(X, y)



X,y = make_moons(n_samples=100, noise=0.15)

polynomial_svm_clf = Pipeline([
    ("poly_features", PolynomialFeatures(degree=3)),
    ("scaler", StandardScaler()),
    ("svm_clf",LinearSVC(C=10, loss="hinge"))

])

polynomial_svm_clf.fit(X,y)

#Kernel funkcija za optimizaciju polinomijalnog SVMa, nije potrebno zadavati pretprocessing korak kao u prethodnom
#skaliranju
polynomial_kernel_svm_clf = Pipeline([
    ("scaler", StandardScaler()),
    ("svm_clf", SVC(kernel="poly", degree=3, coef0=1, C=5))

])

#Similarity features skaliranje feature u odnosu na neki izabrani landmark
#Pristup veliki broj merenja pretvorimo u landmark, mapiramo nove feature u odnosu na sve te nove landmarkove
#uz Kernel magiju uspvamo da fitujemo SVM ludilo kroz sve to(Da bi optimizovali racunanje fita)
#zato sto je Kernel fja efektivna u mapiranju polinomijalnih SVMa
#Gaussian RBF kernel funkcija

rbf_kernel_svm_clf = Pipeline([
    ("scaler", StandardScaler()),
    ("svm_clf", SVC(kernel="rbf", gama=5, C=0.001))

])

#vece Gama uza gama raspodela( uticaj instance koja je landmark je manja na nastanak novih feature-a)
#C na slcian nacin regulise glatkocu granice SVM-a

#SVM za regresiju, prethodno smo SVM koristili za klasifikaciju, sada SVM mozemo da koristimo za
#regresiju, uz izvrtanje problema, gledamo da fitujemo sto vise instanci unutar minimalnog pojasa oko SVM razgranicenja
#dok smo za klasifikaciju gledali maksimalni pojas izmedju klasa

svm_reg = LinearSVR(epsilon=1.5)
#epsilon sirina SVM pojasa klasifikacije
svm_reg.fit(X,y)

#za nelinearne modlee mozemo da koristimo kernelizovan SVM model

svm_poly_reg = SVR(kernel="poly", degree=2, C=100, epsilon=0.1)
svm_poly_reg.fit(X, y)







