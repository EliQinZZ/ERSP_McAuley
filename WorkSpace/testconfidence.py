from sklearn import svm

X = [[1], [2], [3], [4]]
y = [1, 2, 3, 4]

clf = svm.SVC(decision_function_shape='ovr')
clf.fit(X, y)

res = clf.decision_function(X)

print(res)

