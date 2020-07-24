# import the necessary packages
from imutils import build_montages
from datetime import datetime
from time import time
from itertools import chain
import numpy as np
import imagezmq
import argparse
import imutils
import cv2
import face_recognition
import msgpack
import os

import logging
# import matplotlib.pyplot as plt

# from scipy.cluster.hierarchy import dendrogram

from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn import metrics

from numpy import genfromtxt

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", required=True,
  help="Port for the server to which the client will connect")
ap.add_argument("-g", "--gather",
  help="Gather data for training. (0: Smile, 1: Neutral, 2: Frown)")
args = vars(ap.parse_args())

gesture = ['Smiling', 'Neutral', 'Frowning']
clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))

def train():
  print('--------------------------- Training ---------------------------')
  datasets = [genfromtxt(os.path.join('datasets', filename), delimiter=',') for filename in os.listdir('/root/facial_features/datasets') if filename.endswith('.csv')]
  print(f'{len(datasets)} found')

  raw_data = np.concatenate(datasets)

  data = raw_data[1:,1:].astype(float)
  label = raw_data[1:,0].astype(int)

  X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.2, random_state=1)

  clf.fit(X_train, y_train)

  #print test results
  y_pred = clf.predict(X_test)
  print('---------------------- Training Results ----------------------')
  print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
  print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
  print(clf.score(X_test,y_test))
  print('--------------------------------------------------------------')

def predict(keypoints):
  return clf.predict([keypoints])

def gather(action):
  start_server(action)

def normalize(face_landmarks):
  cluster_x = []
  cluster_y = []

  for feature in face_landmarks.keys():
    cluster_x.extend(f[0] for f in face_landmarks[feature])
    cluster_y.extend(f[1] for f in face_landmarks[feature])
  
  # if 'top_lip' in face_landmarks.keys():
  #   cluster_x.extend(f[0] for f in face_landmarks['top_lip'])
  #   cluster_y.extend(f[1] for f in face_landmarks['top_lip'])
  # if 'bottom_lip' in face_landmarks.keys():
  #   cluster_x.extend(f[0] for f in face_landmarks['bottom_lip'])
  #   cluster_y.extend(f[1] for f in face_landmarks['bottom_lip'])

  min_x = cluster_x[0]
  max_x = cluster_x[0]
  for x in cluster_x:
    if(max_x < x): max_x = x
    elif(min_x > x): min_x = x
    
  min_y = cluster_y[0]
  max_y = cluster_y[0]    
  for y in cluster_y:
    if(max_y < y): max_y = y
    elif(min_y > y): min_y = y

  return list(chain.from_iterable((((x-min_x) / (max_x-min_x)) , ((y-min_y) / (max_y - min_y))) for x,y in zip(cluster_x, cluster_y)))

def start_server(action=None):
  print(f'Server Starting on port: {args["port"]}')
  if action is not None:
    print(f'Server is running in gather mode for action: {gesture[action]}')
    gather_file = open(os.path.join('datasets', f'{gesture[action]}{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'),'w')
    
  # initialize the ImageHub object
  imageHub = imagezmq.ImageHub(open_port=f'tcp://*:{args["port"]}')
  print("ImageHub connected")

  frameDict = {}

  # initialize the dictionary which will contain  information regarding
  # when a device was last active, then store the last time the check
  # was made was now
  lastActive = {}
  lastActiveCheck = datetime.now()

  # stores the estimated number of Pis, active checking period, and
  # calculates the duration seconds to wait before making a check to
  # see if a device was active
  ESTIMATED_NUM_PIS = 4
  ACTIVE_CHECK_PERIOD = 10
  ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_PIS * ACTIVE_CHECK_PERIOD

  previousTime = time()
  received = 0
  # start looping over all the frames
  while True:
    if action is not None and time() - previousTime >= 60: # Create new file every minute
      gather_file.close()
      gather_file = open(os.path.join('datasets', f'{gesture[action]}{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'),'w')
      previousTime = time()

    # receive RPi name and frame from the RPi and acknowledge
    # the receipt
    (client, frame) = imageHub.recv_image()
    received += 1
    # print(f'Recieved: {received}')
    
    # if a device is not in the last active dictionary then it means
    # that its a newly connected device
    if client not in lastActive.keys():
      print("[INFO] receiving data from {}...".format(client))

    data = {
      'faces': [],
      'error': ''
    }

    try:
      face_landmarks_list = face_recognition.face_landmarks(frame)
      # print(f"I found {len(face_landmarks_list)} face(s) in this photograph.")

      for face_landmarks in face_landmarks_list:
        face = {
          'features': {},
          'result': ''
        }
        
        keypoints = list()
        if 'top_lip' in face_landmarks.keys():
          face['features']['top_lip'] = face_landmarks['top_lip']
        if 'bottom_lip' in face_landmarks.keys():
          face['features']['bottom_lip'] = face_landmarks['bottom_lip']

        keypoints = normalize(face_landmarks)

        if action is None:
          prediction = predict(keypoints) 
          face['result'] = gesture[int(prediction)]
        else:
          gather_file.write(f'{action},{",".join(map(str, keypoints))}')
          gather_file.write("\n")
          face['result'] = f'Training: {gesture[action]}'

        data['faces'].append(face)
    except Exception as e:
      print(f'An exception occurred: {e}')
      data['error'] = 'Unable to process image'

    imageHub.send_reply(msgpack.packb(data))
    # record the last active time for the device from which we just
    # received a frame
    lastActive[client] = datetime.now()

    # resize the frame to have a maximum width of 400 pixels, then
    # grab the frame dimensions and construct a blob
    # frame = imutils.resize(frame, width=400)
    # (h, w) = frame.shape[:2]
    # blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
    #   0.007843, (300, 300), 127.5)

    # draw the bounding box around the detected object on
    # the frame
    # cv2.rectangle(frame, (startX, startY), (endX, endY),
    #   (255, 0, 0), 2)

    # update the new frame in the frame dictionary
    frameDict[client] = frame

    # if current time *minus* last time when the active device check
    # was made is greater than the threshold set then do a check
    if (datetime.now() - lastActiveCheck).seconds > ACTIVE_CHECK_SECONDS:
      # loop over all previously active devices
      for (client, ts) in list(lastActive.items()):
        # remove the RPi from the last active and frame
        # dictionaries if the device hasn't been active recently
        if (datetime.now() - ts).seconds > ACTIVE_CHECK_SECONDS:
          print("[INFO] lost connection to {}".format(client))
          lastActive.pop(client)
          frameDict.pop(client)
      # set the last active check time as current time
      lastActiveCheck = datetime.now()


if __name__ == '__main__':
  print(args)
  if args['gather'] is None:
    train()
    start_server()
  else:
    try:
      action = int(args['gather'])
      if action < 0 or action > 2:
        print('Action must be one of the following(integer): 0: Smile, 1: Neutral, 2: Frown')
      else:
        gather(action)
    except ValueError:
      print('Action must be one of the following(integer): 0: Smile, 1: Neutral, 2: Frown')

