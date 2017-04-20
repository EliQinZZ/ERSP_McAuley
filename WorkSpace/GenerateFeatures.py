import numpy as np
import math
import gzip
import os
import sys

file_list = []
for file in os.listdir(path='../TrainValidTest'):
    if file.startswith("features_"):
        continue
    if file.endswith(".gz"):
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
    9: Gender
    10: Angle_Avg
    11: Angle_Std
'''

def latlong_to_3d(latr, lonr):
    """Convert a point given latitude and longitude in radians to
    3-dimensional space, assuming a sphere radius of one."""
    return np.array((
        math.cos(latr) * math.cos(lonr),
        math.cos(latr) * math.sin(lonr),
        math.sin(latr)
    ))

def angle_between_vectors_degrees(u, v):
    """Return the angle between two vectors in any dimension space,
    in degrees."""

    num_to_acos = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

    if num_to_acos < -1 or num_to_acos > 1:
        return -999

    return np.rad2deg(
        math.acos(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))))


def generate_angle_list(latitude_list, longitude_list):
    if len(latitude_list) <= 2:
        return [0]

    angle_list = []

    for i in range(len(latitude_list)):
        if i + 2 >= len(latitude_list):
            break

        curr_points = [
            (latitude_list[i], longitude_list[i]),
            (latitude_list[i + 1], longitude_list[i + 1]),
            (latitude_list[i + 2], longitude_list[i + 2]),
        ]

        calculated_angle = calculate_angle(curr_points)
        if calculated_angle != -999:
            angle_list.append(calculated_angle)

    return angle_list


def calculate_angle(points):
    A = points[0]
    B = points[1]
    C = points[2]

    # Convert the points to numpy latitude/longitude radians space
    a = np.radians(np.array(A))
    b = np.radians(np.array(B))
    c = np.radians(np.array(C))

    # Vectors in latitude/longitude space
    avec = a - b
    cvec = c - b

    # Adjust vectors for changed longitude scale at given latitude into 2D space
    lat = b[0]
    avec[1] *= math.cos(lat)
    cvec[1] *= math.cos(lat)

    # Find the angle between the vectors in 2D space
    angle2deg = angle_between_vectors_degrees(avec, cvec)

    return angle2deg


def generate_features(curr_dic):

    angle_list = generate_angle_list(curr_dic['latitude'], curr_dic['longitude'])

    features = [np.amin(curr_dic['speed']),
                np.mean(curr_dic['speed']),
                np.amax(curr_dic['speed']),
                np.std(curr_dic['speed']),
                np.amin(curr_dic['heart_rate']),
                np.mean(curr_dic['heart_rate']),
                np.amax(curr_dic['heart_rate']),
                np.ptp(curr_dic['heart_rate']),
                np.ptp(curr_dic['altitude']),
                curr_dic['gender'],
                np.mean(angle_list),
                np.std(angle_list)
                ]
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
    zout = gzip.open('../TrainValidTest/features_' + file, 'wb')
    for feature in feature_list:
        zout.write(bytes(str(feature) + '\n', 'ascii'))
    zout.close()
