from sklearn.feature_extraction.text import HashingVectorizer
#from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
import sklearn.cross_validation
import reading as rd
from preprocess import Tokenizer


vectorizer_hash = HashingVectorizer(tokenizer=Tokenizer(), lowercase=True, strip_accents='unicode', stop_words='english', ngram_range=(1, 3))

score1 =0.0
score2 =0.0

for i in range(0,5):
	Xtrain, Xtest, y_train, y_test = sklearn.cross_validation.train_test_split(rd.dataset, rd.target, test_size=0.2)

	X_train = vectorizer_hash.transform(Xtrain)
	X_test = vectorizer_hash.transform(Xtest)

	#SVM with SGD
	clf = LinearSVC(loss='l2', penalty='l2', dual=False, tol=1e-3)

	clf.fit(X_train, y_train)

	pred = clf.predict(X_test)
	print(metrics.confusion_matrix(y_test, pred))

	temp1 = metrics.accuracy_score(y_test, pred)
	score1 += temp1
	print temp1
	'''
	clf = LinearSVC(loss='l2', penalty='l1', dual=False, tol=1e-3)

	clf.fit(X_train, y_train)

	pred = clf.predict(X_test)
	print(metrics.confusion_matrix(y_test, pred))

	temp2 = metrics.accuracy_score(y_test, pred)
	score += temp2
	print temp2
	'''

print "Final", (score1/5)

