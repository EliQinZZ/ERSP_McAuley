import gzip
from sklearn import svm


feature_low_bound = 0
feature_high_bound = 3
c_list = [1]


def read_file(fin, low_bound, high_bound):

    feature_list = []
    result_list = []

    for l in fin:
        l = l.decode('ascii')
        curr_list = eval(l)
        feature_list.append(curr_list[0][low_bound:high_bound])
        result_list.append(curr_list[1])

    return[feature_list, result_list]


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

train_list = read_file(tin, feature_low_bound, feature_high_bound)
valid_list = read_file(vin, feature_low_bound, feature_high_bound)

vin.close()
tin.close()

print("Finished reading")

X_train = train_list[0]
y_train = train_list[1]

X_valid = valid_list[0]
y_valid = valid_list[1]

print("Features are from index {} to index {}".format(feature_low_bound, feature_high_bound))
print("# of training data is {}".format(len(X_train)))
print("# of validation data is {}".format(len(X_valid)))

train_corr_list = []
valid_corr_list = []

print("Begin with decision function OVR\n")

for c in c_list:
    print("Begin with c = {}".format(c))
    clf = svm.SVC(kernel='linear', C=c, decision_function_shape='ovr')
    clf.fit(X_train, y_train)

    train_predictions = clf.predict(X_train)
    valid_predictions = clf.predict(X_valid)

    train_corr = correctness(train_predictions, y_train)
    valid_corr = correctness(valid_predictions, y_valid)

    train_corr_list.append(train_corr)
    valid_corr_list.append(valid_corr)

    log_ovr.write(str(train_predictions) + "\n")
    log_ovr.write(str(valid_predictions) + "\n")

    print("Train correctness: {:.6}\tValid correctness: {:.6}\n".format(train_corr, valid_corr))

log_ovr.close()


print("Begin with decision function OVO\n")
train_corr_list = []
valid_corr_list = []

for c in c_list:
    print("Begin with c = {}".format(c))
    clf = svm.SVC(kernel='linear', C=c, decision_function_shape='ovo')
    clf.fit(X_train, y_train)

    train_predictions = clf.predict(X_train)
    valid_predictions = clf.predict(X_valid)

    train_corr = correctness(train_predictions, y_train)
    valid_corr = correctness(valid_predictions, y_valid)

    train_corr_list.append(train_corr)
    valid_corr_list.append(valid_corr)

    log_ovo.write(str(train_predictions) + "\n")
    log_ovo.write(str(valid_predictions) + "\n")

    print("Train correctness: {:.6}\tValid correctness: {:.6}\n".format(train_corr, valid_corr))

log_ovr.close()

