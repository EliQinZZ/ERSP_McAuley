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


def read_file(fin):

    feature_list = []
    result_list = []

    for l in fin:
        l = l.decode('ascii')
        curr_list = eval(l)
        feature_list.append(curr_list[0])
        result_list.append(curr_list[1])

    return[feature_list, result_list]


def perform_experiment(c_value, decision_function, log_file):
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
    print("Train correctness: {:.6}\tValid correctness: {:.6}\n".format(train_corr, valid_corr))


def correctness(pred, real):
    total = 0
    corr = 0
    for i in range(len(pred)):
        total += 1
        if pred[i] == real[i]:
            corr += 1

    return corr / total

log_ovr = open('MultiClassifierTop8LogOvr', 'w')
log_ovo = open('MultiClassifierTop8LogOvo', 'w')

tin = gzip.open('../TrainValidTest/feature_training_set_top_8.json.gz', 'rb')
vin = gzip.open('../TrainValidTest/feature_validation_set_top_8.json.gz', 'rb')

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

    for features in train_list:
        curr_train_features = []
        curr_valid_features = []
        for index in feature_indexes:
            curr_train_features.append(train_list[0][index])
            curr_valid_features.append(valid_list[0][index])
        X_train.append(curr_train_features)
        X_valid.append(curr_valid_features)

    print("# of training data is {}".format(len(X_train)))
    print("# of validation data is {}".format(len(X_valid)))

    train_corr_list = []
    valid_corr_list = []

    print("Begin with decision function OVR\n")

    for c in c_list:
        print("Begin with c = {}".format(c))
        perform_experiment(c, 'ovr', log_ovr)

    log_ovr.close()

    print("Begin with decision function OVO\n")

    for c in c_list:
        print("Begin with c = {}".format(c))
        perform_experiment(c, 'ovo', log_ovo)

    log_ovr.close()

