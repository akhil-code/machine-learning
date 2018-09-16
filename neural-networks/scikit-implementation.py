from sklearn import datasets
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib


digits = datasets.load_digits()

X, y = digits.data, digits.target

print(f"training dataset size: {len(y)}")

classifier = MLPClassifier(
    solver='lbfgs',
    alpha=1e-5,
    hidden_layer_sizes=(10, 10, 10),
    random_state=1,
    max_iter=1000000,
)

classifier.fit(X, y)

joblib.dump(classifier, 'pickles/mlp-digits.pkl')

predicted = classifier.predict(X[-1:])
actual = digits.target[-1]

print(f"actual: {actual}, predicted: {predicted}")