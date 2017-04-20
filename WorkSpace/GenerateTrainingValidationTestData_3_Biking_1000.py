# This file splits the run/bike data into training, validation and test dataset, and generates corresponding files
from random import shuffle
import gzip

sportlist = ["bike_cleaned.json.gz", "bike (transport)_cleaned.json.gz", "mountain bike_cleaned.json.gz"]

# Set the ratio among sizes of training/validation/test dataset
train_percent = 1 / 3
validation_percent = 1 / 3
test_percent = 1 / 3

workout_list = []
total_workout = 0
# Put the workout data into workout_list
for sportfile in sportlist:
    count = 0
    with gzip.open("../CleaningWithSpeed/" + sportfile, 'r') as file:
        for workout in file:
            if (count >= 1000):
                break
            workout_list.append(workout)
            total_workout += 1
            count += 1
    8
print("Finished reading \n")
shuffle(workout_list)
print("Finished shuffling \n")

# Calculate sizes of training/validation/test dataset
train_size = int(train_percent * total_workout)
validation_size = int(validation_percent * total_workout)
test_size = total_workout - train_size - validation_size

print("Size of total workout is %d \n" % total_workout)
print("Size of training set is %d \n" % train_size)
print("Size of validation set is %d \n" % validation_size)
print("Size of test set is %d \n" % test_size)

# Split the workout data according to the calculated sizes above
# Note: slicing ":" is left-inclusive and right-exclusive
train_list = workout_list[:train_size]
validation_list = workout_list[train_size: train_size + validation_size]
test_list = workout_list[train_size + validation_size:]

# Write into separate files
with gzip.open("../TrainValidTest/training_set_3_biking_1000.json.gz", 'wb') as file1:
    for workout in train_list:
        file1.write(workout)
print("Finished writing training set\n")

with gzip.open("../TrainValidTest/validation_set_3_biking_1000.json.gz", 'wb') as file2:
    for workout in validation_list:
        file2.write(workout)
print("Finished writing validation set\n")

with gzip.open("../TrainValidTest/test_set_3_biking_1000.json.gz", 'wb') as file3:
    for workout in test_list:
        file3.write(workout)
print("Finished writing test set\n")