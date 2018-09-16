from sklearn.externals import joblib
from sklearn import datasets, svm
import pickle


# datasets
digits = datasets.load_digits()

# training SVM classifier for digits
classifier = svm.SVC(gamma=0.001, C=100.)
classifier.fit(digits.data[:-1], digits.target[:-1])

# making persistance model
joblib.dump(classifier, 'pickles/svc-digits.pkl')
