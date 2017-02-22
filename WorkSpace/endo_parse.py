import gzip
import os
import time
import datetime
import random

def toUnix(timestamp):
  return int(time.mktime(datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.000Z").timetuple()))

zout = gzip.open('endomondo.json.gz', 'wb')
zout2 = gzip.open('endomondoHR.json.gz', 'wb')

fs = os.listdir()
random.shuffle(fs)

for f in os.listdir():
  if not (".txt.gz" in f): continue
  z = gzip.open(f, 'r')
  d = {}
  l = z.readline().decode('ascii')
  userId,gender = l.strip().split()
  d['userId'] = int(userId)
  print(f)
  print("Processing user " + str(userId) + ' (' + "https://www.endomondo.com/profile/" + userId + '/)')
  d['gender'] = {0:"male", 1:"female", 2:"unknown"}[int(gender)]
  for l in z:
    l = l.decode('ascii')
    d1 = dict(d)
    run = eval(l)
    d1['id'] = run['id']
    d1['url'] = "https://www.endomondo.com/users/" + str(userId) + "/workouts/" + str(run['id'])
    print("  Processing workout " + d1['url'])
    try:
      d1['sport'] = {36: 'handball',
                   34: 'rugby',
                   29: 'cricket',
                   44: 'beach volleyball',
                   89: 'skateboarding',
                   25: 'baseball',
                   48: 'martial arts',
                   45: 'volleyball',
                   8: 'snowboarding',
                   37: 'hockey',
                   94: 'treadmill walking',
                   31: 'dancing',
                   26: 'basketball',
                   93: 'climbing',
                   43: 'tennis',
                   33: 'american football',
                   15: 'golf',
                   27: 'boxing',
                   10: 'kite surfing',
                   91: 'snowshoeing',
                   28: 'stair climing',
                   47: 'yoga',
                   92: 'wheelchair',
                   87: 'circuit training',
                   38: 'pilates',
                   7: 'downhill skiing',
                   30: 'elliptical',
                   24: 'badminton',
                   23: 'aerobics',
                   5: 'roller skiing',
                   50: 'step counter',
                   12: 'sailing',
                   13: 'windsurfing',
                   88: 'treadmill running',
                   49: 'gymnastics',
                   9: 'kayaking',
                   17: 'orienteering',
                   11: 'rowing',
                   19: 'horseback riding',
                   35: 'soccer',
                   46: 'weight training',
                   14: 'fitness walking',
                   16: 'hiking',
                   21: 'indoor cycling',
                   22: 'core stability training',
                   20: 'swimming',
                   4: 'skate',
                   0: 'run',
                   40: 'scuba diving',
                   1: 'bike (transport)',
                   2: 'bike',
                   3: 'mountain bike',
                   18: 'walk',
                   41: 'squash',
                   42: 'table tennis',
                   90: 'surfing',
                   39: 'polo',
                   32: 'fencing',
                   86: 'walk (transport)',
                   84: 'weight lifting',
                   58: 'circuit training',
                   6: 'cross-country skiing'}[run['sport']]
      if '?' in d1['sport']:
        print("CHECK " + str(run['sport']) + ' ' + d1['sport'])
    except Exception as e:
      print("CHECK: Unknown sport " + str(run['sport']))
    if not 'points' in run or not run['points'] or not 'points' in run['points']:
      print("  Run has no temporal data, skipping")
      continue
    pts = [p for p in run['points']['points'] if len(p['sensor_data'])]
    if not len(pts):
      print("  Run has no sensor info, skipping")
      continue
    try:
      d1['speed'] = [x['sensor_data']['speed'] for x in pts]
    except Exception as e:
      print("  Run has no pace data")
    try:
      d1['heart_rate'] = [x['sensor_data']['heart_rate'] for x in pts]
    except Exception as e:
      print("  Run has no hr data")
    for g in ['altitude', 'longitude', 'latitude']:
      try:
        d1[g] = [x[g] for x in pts]
      except Exception as e:
        print("  Run has no GPS data")
    try:
      d1['timestamp'] = [toUnix(x['time']) for x in pts]
    except Exception as e:
      print("  Run has no timestamp")
      continue
    isGood = 'heart_rate' in d1 and 'altitude' in d1 and 'latitude' in d1 and 'longitude' in d1
    zout.write(bytes(str(d1) + '\n', 'ascii'))
    if isGood:
      zout2.write(bytes(str(d1) + '\n', 'ascii'))
