import numpy as np
import gzip
import os

from math import acos
from math import sqrt
from math import pi

file_list = []
for file in os.listdir(path='../TrainValidTest'):
    if file.startswith("features_"):
        continue
    if file.endswith(".gz"):
        file_list.append(file)
file_list = ["validation_set_top4_1000.json.gz", "training_set_top4_1000.json.gz", "test_set_top4_1000.json.gz"]
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
'''

def generate_features(curr_dic):

    angle_list = generate_avg_angle_change_feature(curr_dic)

    features = [np.amin(curr_dic['speed']),
                np.mean(curr_dic['speed']),
                np.amax(curr_dic['speed']),
                np.std(curr_dic['speed']),
                np.amin(curr_dic['heart_rate']),
                np.mean(curr_dic['heart_rate']),
                np.amax(curr_dic['heart_rate']),
                np.ptp(curr_dic['heart_rate']),
                np.ptp(curr_dic['altitude']),
                {'unknown': 0, 'male': 1, 'female': 2}[curr_dic['gender']],
                np.std(angle_list)
                ]
    return features


def generate_avg_angle_change_feature(workout):

    angle_list1 = []
    # angle_list2 = []

    longitude_list = workout['longitude']
    latitude_list = workout['latitude']

    for i in range(0, len(longitude_list) - 2):
        vector1 = [longitude_list[i + 1] - longitude_list[i], latitude_list[i + 1] - latitude_list[i]]
        vector2 = [longitude_list[i + 2] - longitude_list[i + 1], latitude_list[i + 2] - latitude_list[i + 1]]
        clockwise_angle = angle_clockwise(vector1, vector2)
        if clockwise_angle == 360:
            clockwise_angle = 0
        # first method
        angle1 = clockwise_angle
        angle_list1.append(angle1)

        # second method
        # if clockwise_angle > 180:
        #     clockwise_angle = 360 - clockwise_angle
        # angle2 = clockwise_angle
        # angle_list2.append(angle2)

    return angle_list1


def length(v):
    return sqrt(v[0]**2 + v[1]**2)


def dot_product(v, w):
    return v[0]*w[0]+v[1]*w[1]


def determinant(v, w):
    return v[0]*w[1]-v[1]*w[0]


def inner_angle(v,w):
    if length(v) == 0 or length(w) == 0:
        return 0
    cos_x = dot_product(v, w)/(length(v)*length(w))
    if cos_x > 1:
        cos_x = 1
    if cos_x < -1:
        cos_x = -1
    rad = acos(cos_x)  # in radians
    return rad*180/pi  # returns degrees

# return the clockwise angle from A to B
def angle_clockwise(A, B):
    inner = inner_angle(A, B)
    det = determinant(A, B)
    if det < 0:  # This is a property of the det. If the det < 0 then B is clockwise of A
        return inner
    else:  # If the det > 0 then A is immediately clockwise of B
        return 360-inner

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
    zout = gzip.open('../TrainValidTest/features_' + file, 'wb')
    for feature in feature_list:
        zout.write(bytes(str(feature) + '\n', 'ascii'))
    zout.close()
