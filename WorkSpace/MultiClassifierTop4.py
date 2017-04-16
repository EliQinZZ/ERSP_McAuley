import gzip
from sklearn import svm

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
'''
experiments = [
    [1, 3, 8],
    [1, 3, 8, 0, 2],
    [1, 3, 8, 0, 2, 7],
    [1, 3, 8, 0, 2, 7, 5],
]
c_list = [1]

tout = gzip.open('../MulticlassTop4ResultTrain.gz', 'wb')
vout = gzip.open('../MulticlassTop4ResultValid.gz', 'wb')

def read_file(fin):

    feature_list = []
    result_list = []

    for l in fin:
        l = l.decode('ascii')
        curr_list = eval(l)
        feature_list.append(curr_list[0])
        result_list.append(curr_list[1])

    return[feature_list, result_list]


def perform_experiment(X_train, y_train, X_valid, y_valid, c_value, decision_function, log_file):
    clf = svm.SVC(kernel='linear', C=c_value, decision_function_shape=decision_function)
    clf.fit(X_train, y_train)
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
log_ovo = open('MultiClassifierTop4LogOvo', 'w')

tin = gzip.open('../TrainValidTest/features_training_set_top_4.json.gz', 'rb')
vin = gzip.open('../TrainValidTest/features_validation_set_top_4.json.gz', 'rb')

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
            curr_valid_features.append(valid_list[0][index])
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

    print("Begin with decision function OVO\n")

    for c in c_list:
        print("Begin with c = {}".format(c))
        perform_experiment(X_train, y_train, X_valid, y_valid, c, 'ovo', log_ovo)

    log_ovr.close()

tout.close()
vout.close()
print("Finished.")
