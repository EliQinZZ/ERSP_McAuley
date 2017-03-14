import numpy
from sklearn import svm
import gzip
from sklearn.model_selection import cross_val_score


def generate_features(data_ist):
    feature_list = []
    for data in data_ist:
        curr_features = []
        curr_features.append(numpy.amin(data['speed']))
        curr_features.append(numpy.mean(data['speed']))
        curr_features.append(numpy.amax(data['speed']))
        curr_features.append(numpy.amin(data['heart_rate']))
        curr_features.append(numpy.mean(data['heart_rate']))
        curr_features.append(numpy.amax(data['heart_rate']))

        feature_list.append(curr_features)
    return feature_list

print("Reading data...")
tin = gzip.open('../RunningBikingTrainValidTest/cross_validation_set_running_and_biking.json.gz', 'rb')

train_list = []

for l in tin:
    l = l.decode('ascii')
    dic = eval(l)
    train_list.append(dic)

print("done")

X_train_list = generate_features(train_list)
y_train_list = [b['sport'] is 'run' for b in train_list]

print("Starting")


print("Features are speed and HR")
print("kernel is linear")

c_list = [10, 100, 500, 1000, 1500, 2000]

for c in c_list:
    clf = svm.SVC(kernel='linear', C=c)
    scores = cross_val_score(clf, X_train_list, y_train_list, cv=5)

    print("C is {}".format(c))
    print(scores)
    print("Accuracy: %0.6f (+/- %0.6f)" % (scores.mean(), scores.std() * 2))

