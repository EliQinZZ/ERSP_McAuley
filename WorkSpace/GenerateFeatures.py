import numpy
import gzip

file_list = ['training_set_top_8.json.gz', 'validation_set_top_8.json.gz']


def generate_features(curr_dic):
    features = [numpy.amin(curr_dic['speed']),
                numpy.mean(curr_dic['speed']),
                numpy.amax(curr_dic['speed']),
                numpy.amin(curr_dic['heart_rate']),
                numpy.mean(curr_dic['heart_rate']),
                numpy.amax(curr_dic['heart_rate'])]
    return features


for file in file_list:

    print("Processing " + file)
    zin = gzip.open('../TrainValidTest/' + file, 'rb')

    print("Generating features for " + file)
    feature_list = []
    for l in zin:
        l = l.decode('ascii')
        dic = eval(l)
        feature_list.append([generate_features(dic), dic['sport']])
    zin.close()

    print("Writing features for " + file)
    zout = gzip.open('../TrainValidTest/feature_' + file, 'wb')
    for feature in feature_list:
        zout.write(bytes(str(feature) + '\n', 'ascii'))
    zout.close()
