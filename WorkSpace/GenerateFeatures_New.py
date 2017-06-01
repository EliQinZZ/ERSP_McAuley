import numpy as np
import gzip
import os

import math
from math import acos
from math import sqrt
from math import pi

file_list = []
'''
for file in os.listdir(path='../TrainValidTest'):
    if file.startswith("features_"):
        continue
    if file.endswith(".gz"):
        file_list.append(file)
'''

file_list = ["test_set_top4_1000.json.gz"]


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
    11: displacement/distance
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
                np.std(angle_list),
                generateRatio(curr_dic)
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


# -------------------------new feature---------
def displacementOfTwoPoints(x1, y1, x2, y2):
    x = math.pow((y1 - y2), 2)
    y = math.pow((x1 - x2), 2)
    return math.sqrt(x + y)

def findCountProportion(threshold, user):
    count = 0
    total = 0
    result= 0
    for eachPoint in user:
        ratiolist = user[eachPoint]
        for ratio in ratiolist:
            if ratio <= threshold:
                count = count + 1
            total = total + 1
    if total != 0:
        result = count / total
    print('done')
    return result

def generateRatio(workout):
    pair = []
    pair.append(workout["longitude"])
    pair.append(workout["latitude"])

    print("constructing ratio...")
    same_point_count = 0;
    dispOverDistance = {}
    # print('{} {} {}'.format('sequence,','point,', 'length of ratio list'))
    for i in range(10, len(pair[0])):
        currentpoint_x = pair[0][i]
        currentpoint_y = pair[1][i]
        ratio = []
        # form a list of ratio to the point
        for k in range(0, i - 10):
            distance = 0;
            for p in range(k, i):
                distance = distance + displacementOfTwoPoints(pair[0][p], pair[1][p], pair[0][p + 1], pair[1][p + 1])
            displacement = displacementOfTwoPoints(pair[0][k], pair[1][k], pair[0][i], pair[1][i])
            if distance != 0.0:
                ratio.append(displacement / distance)
            else:
                same_point_count = same_point_count + 1
        dispOverDistance[(currentpoint_x, currentpoint_y)] = ratio;
    return findCountProportion(0.5, dispOverDistance)



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
    zout = gzip.open('../TrainValidTestNew/features_' + file, 'wb')
    for feature in feature_list:
        zout.write(bytes(str(feature) + '\n', 'ascii'))
    zout.close()