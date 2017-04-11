import gzip
import os
from random import shuffle

# Set the ratio among sizes of training/validation/test data set
train_percent = 0.42
validation_percent = 0.18
test_percent = 0.40

workout_list = []
total_workout = 0

for f in os.listdir(path='../CleaningWithSpeed/Top4'):
    zin = gzip.open('../CleaningWithSpeed/' + f, 'rb')

    print('Reading ' + f)
    for workout in zin:
        total_workout += 1
        workout_list.append(workout)

    zin.close()

print("Finished reading; Total read in is {:d}\n".format(total_workout))

shuffle(workout_list)

print("Finished shuffling.\n")

# Calculate sizes of training/validation/test data set
train_size = int(train_percent * total_workout)
validation_size = int(validation_percent * total_workout)
test_size = total_workout - train_size - validation_size

print("Size of total workout for top 4 is {:d}".format(total_workout))
print("Size of training set for top 4 is {:d}".format(train_size))
print("Size of validation set for top 4 is {:d}".format(validation_size))
print("Size of test set for top 4 is {:d}\n".format(test_size))

# Split the workout data according to the calculated sizes above
# Note: slicing ":" is left-inclusive and right-exclusive
train_list = workout_list[:train_size]
validation_list = workout_list[train_size: train_size + validation_size]
test_list = workout_list[train_size + validation_size:]

# Write into separate files
tr_out = gzip.open("../TrainValidTest/training_set_top_4.json.gz", 'wb')
va_out = gzip.open("../TrainValidTest/validation_set_top_4.json.gz", 'wb')
te_out = gzip.open("../TrainValidTest/test_set_top_4.json.gz", 'wb')

for workout in train_list:
    tr_out.write(workout)
print("Finished writing training set for top 4")

for workout in validation_list:
    va_out.write(workout)
print("Finished writing validation set for top 4")

for workout in test_list:
    te_out.write(workout)
print("Finished writing test set for top 4")

tr_out.close()
va_out.close()
te_out.close()
