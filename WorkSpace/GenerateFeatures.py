import numpy
import gzip
import os

file_list = []
for file in os.listdir(path='../TrainValidTestTemp'):
    file_list.append(file)

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


def generate_features(curr_dic):
    features = [numpy.amin(curr_dic['speed']),
                numpy.mean(curr_dic['speed']),
                numpy.amax(curr_dic['speed']),
                numpy.std(curr_dic['speed']),
                numpy.amin(curr_dic['heart_rate']),
                numpy.mean(curr_dic['heart_rate']),
                numpy.amax(curr_dic['heart_rate']),
                numpy.ptp(curr_dic['heart_rate']),
                numpy.ptp(curr_dic['altitude'])
                ]
    return features


for file in file_list:

    print("Processing " + file)
    zin = gzip.open('../TrainValidTestTemp/' + file, 'rb')

    print("Generating features for " + file)
    feature_list = []
    for l in zin:
        l = l.decode('ascii')
        dic = eval(l)
        feature_list.append([generate_features(dic), dic['sport']])
    zin.close()

    print("Writing features for " + file)
    zout = gzip.open('../TrainValidTestTemp/features_' + file, 'wb')
    for feature in feature_list:
        zout.write(bytes(str(feature) + '\n', 'ascii'))
    zout.close()
