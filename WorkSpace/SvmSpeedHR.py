import numpy
from sklearn import svm
import gzip
from datetime import datetime


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

def correctness(pred, real):
    total = 0
    errors = 0
    for i in range(len(pred)):
        total += 1
        if pred[i] != real[i]:
            errors += 1

    return 1 - errors / total

print("Reading data...")

tin = gzip.open('../RunningBikingTrainValidTest/training_set_running_and_biking.json.gz', 'rb')
vin = gzip.open('../RunningBikingTrainValidTest/validation_set_running_and_biking.json.gz', 'rb')

train_list = []
valid_list = []

for l in tin:
    l = l.decode('ascii')
    dic = eval(l)
    train_list.append(dic)
for l in vin:
    l = l.decode('ascii')
    dic = eval(l)
    valid_list.append(dic)

tin.close()
vin.close()

print("done")

X_train_list = generate_features(train_list)
y_train_list = [b['sport'] is 'run' for b in train_list]
X_valid_list = generate_features(valid_list)
y_valid_list = [b['sport'] is 'run' for b in valid_list]

print("Starting")
print("kernel is linear")
print("Features are Min, Avg and Max of speed and HR")

c_list = [1, 10, 100, 500, 1000, 1500, 2000]

train_errors = []
valid_errors = []
for c in c_list:
    print("Running for c = " + str(c))
    clf = svm.SVC(kernel='linear', C=c)
    start = datetime.now()
    clf.fit(X_train_list, y_train_list)
    print("Time for fitting is " + str(datetime.now() - start))

    train_predictions = clf.predict(X_train_list)
    valid_predictions = clf.predict(X_valid_list)

    train_errors.append(correctness(train_predictions, y_train_list))
    valid_errors.append(correctness(valid_predictions, y_valid_list))

    print("{:.6}\t{:.6}".format(train_errors[len(train_errors) - 1], valid_errors[len(valid_errors) - 1]))

