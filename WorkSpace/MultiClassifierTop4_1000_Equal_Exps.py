import gzip
from sklearn import svm
from datetime import datetime


'''
Feature index:
    0: Speed_Min
    1: Speed_Avg
    2: Speed_Max
    3: Speed_Std
    4: HR_Min
    5: HR_Avg
    6: HR_Max
    7: HR_Range
    8: Altitude_Range
    9: Gender
    10: Angle_Std
    11: DOD
'''
experiments = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
]
c_list = [1]

tout = gzip.open('../MultiClassifierResults/TrainBikes1000.gz', 'wb')
vout = gzip.open('../MultiClassifierResults/ValidBikes1000.gz', 'wb')

def read_file(fin):

    feature_list = []
    result_list = []

#    num_data = 0

    for l in fin:
        l = l.decode('ascii')
        curr_list = eval(l)
        feature_list.append(curr_list[0])
        result_list.append(curr_list[1])
#        num_data += 1
#        if num_data == 1000:
#            break

    return[feature_list, result_list]


def perform_experiment(X_train, y_train, X_valid, y_valid, c_value, decision_function, log_file):
    clf = svm.SVC(kernel='linear', C=c_value, decision_function_shape=decision_function)
    start = datetime.now()
    clf.fit(X_train, y_train)
    print("Time for fitting is " + str(datetime.now() - start))
    train_predictions = clf.predict(X_train)
    valid_predictions = clf.predict(X_valid)
    train_corr = correctness(train_predictions, y_train)
    valid_corr = correctness(valid_predictions, y_valid)
    train_corr_list.append(train_corr)
    valid_corr_list.append(valid_corr)
    log_file.write(str(train_predictions) + "\n")
    log_file.write(str(valid_predictions) + "\n")
    tout.write(bytes(str(y_train) + "\n" + str(list(train_predictions)) + "\n", 'ascii'))
    vout.write(bytes(str(y_valid) + "\n" + str(list(valid_predictions)) + "\n", 'ascii'))
    print("Train correctness: {:.6}\tValid correctness: {:.6}\n".format(train_corr, valid_corr))


def correctness(pred, real):
    total = 0
    corr = 0
    for i in range(len(pred)):
        total += 1
        if pred[i] == real[i]:
            corr += 1

    return corr / total

log_ovr = open('MultiClassifierTop4LogOvr', 'w')

tin = gzip.open('../TrainValidTest/features_training_set_3_biking_1000.json.gz', 'rb')
vin = gzip.open('../TrainValidTest/features_validation_set_3_biking_1000.json.gz', 'rb')

print("Reading files")

train_list = read_file(tin)
valid_list = read_file(vin)

vin.close()
tin.close()

print("Finished reading")

for feature_indexes in experiments:

    print("Begging experiment with feature indexes " + str(feature_indexes))

    X_train = []
    y_train = train_list[1]
    X_valid = []
    y_valid = valid_list[1]

    print("Constructing training and validation features")

    for features in train_list[0]:
        curr_train_features = []
        for index in feature_indexes:
            curr_train_features.append(features[index])
        X_train.append(curr_train_features)

    for features in valid_list[0]:
        curr_valid_features = []
        for index in feature_indexes:
            curr_valid_features.append(features[index])
        X_valid.append(curr_valid_features)

    print("# of training data is {}".format(len(X_train)))
    print("# of validation data is {}".format(len(X_valid)))

    train_corr_list = []
    valid_corr_list = []

    print("Begin with decision function OVR\n")

    for c in c_list:
        print("Begin with c = {}".format(c))
        perform_experiment(X_train, y_train, X_valid, y_valid, c, 'ovr', log_ovr)




log_ovr.close()
tout.close()
vout.close()
print("Finished.")
