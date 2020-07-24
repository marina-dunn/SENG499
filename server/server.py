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
args = vars(ap.parse_args())

gesture = ['Smiling', 'Neutral', 'Frowning']

smile = genfromtxt('./datasets/smile.csv', delimiter=',')
neutral = genfromtxt('./datasets/neutral.csv', delimiter=',')
frown = genfromtxt('./datasets/frown.csv', delimiter=',')

raw_data = np.concatenate((smile,neutral,frown))

data = raw_data[1:,1:].astype(float)
label = raw_data[1:,0].astype(int)

X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.2, random_state=1)

clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
clf.fit(X_train, y_train)

#print test results
y_pred = clf.predict(X_test)
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print(clf.score(X_test,y_test))


def predict(keypoints):
  return clf.predict([keypoints])

def start_server():
  print(f'Server Starting on port: {args["port"]}')
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

  # start looping over all the frames
  while True:
    # receive RPi name and frame from the RPi and acknowledge
    # the receipt
    (client, frame) = imageHub.recv_image()
    
    # if a device is not in the last active dictionary then it means
    # that its a newly connected device
    if client not in lastActive.keys():
      print("[INFO] receiving data from {}...".format(client))

    print("Frame received")

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
        for facial_feature in face_landmarks.keys():
          if(facial_feature == 'top_lip' or facial_feature == 'bottom_lip'):
            face['features'][facial_feature] = face_landmarks[facial_feature]
            
            keypoints.extend(list(chain.from_iterable((x[0], x[1]) for x in  face_landmarks[facial_feature])))
        print(keypoints)
        prediction = predict(keypoints) 

        face['result'] = gesture[int(prediction)]
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
  start_server()
