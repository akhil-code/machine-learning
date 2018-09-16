from sklearn import datasets, svm
from sklearn.externals import joblib

# loading iris dataset
iris = datasets.load_iris()
X, y = iris.data, iris.target

# creating classifier object
classifier = svm.SVC()
# training classifier
classifier.fit(X, y)

# saving a persistance model
joblib.dump(classifier, 'pickles/svc-iris.pkl')
