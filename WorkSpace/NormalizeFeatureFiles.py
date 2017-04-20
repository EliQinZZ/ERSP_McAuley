import os
from sklearn import preprocessing
import gzip

num_feature = 11

feature_list = []

for i in range(11):
    feature_list.append([])


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

file_list = []
for file in os.listdir(path='../TrainValidTest'):
    if file.startswith("features_"):
        file_list.append(file)

for file in file_list:

    print("Processing " + file)

    zin = gzip.open('../TrainValidTest/' + file, 'rb')

    workout_types = []

    for l in zin:
        l.decode('ascii')
        dic = eval(l)

        features = l[0]


        for i in range(len(features)):
            if isfloat(features[i]):
                feature_list[i].append(float[features[i]])
            else:
                feature_list[i].append(features[i])

        workout_types.append(l[1])

    for feature in feature_list:
        feature = preprocessing.normalize(feature)

    zout = gzip.open('../TrainValidTest/normalized_' + file, 'wb')
    for i in range(len(feature_list[0])):
        curr_features = []
        for j in range(len(feature_list)):
            curr_features.append(feature_list[j][i])
        output_list = [curr_features, workout_types[i]]
        zout.write(bytes(str(output_list) + '\n', 'ascii'))

    zin.close()
    zout.close()