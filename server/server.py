# import the necessary packages
from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2
import face_recognition
import msgpack

print("Server Starting")
# initialize the ImageHub object
imageHub = imagezmq.ImageHub(open_port='tcp://*:40005')
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
  print("Frame received")
  face_landmarks_list = face_recognition.face_landmarks(frame)
  data = []
  print(f"I found {len(face_landmarks_list)} face(s) in this photograph.")
  imageHub.send_reply(b'Ok')

  # for face_landmarks in face_landmarks_list:
  #   face = {
  #     'features': {}
  #   }
  #   for facial_feature in face_landmarks.keys():
  #     if(facial_feature == 'top_lip' or facial_feature == 'bottom_lip'):
  #       face['features'][facial_feature] = face_landmarks[facial_feature]
  #       # for points in face_landmarks[facial_feature]:
  #       #   output = f"{output}\n {points[0]},{points[1]}\n"
  #   data.append(face)

  # imageHub.send_reply(msgpack.packb(data))
  # # if a device is not in the last active dictionary then it means
  # # that its a newly connected device
  # if client not in lastActive.keys():
  #   print("[INFO] receiving data from {}...".format(client))
  # # record the last active time for the device from which we just
  # # received a frame
  # lastActive[client] = datetime.now()

  # # resize the frame to have a maximum width of 400 pixels, then
	# # grab the frame dimensions and construct a blob
  # # frame = imutils.resize(frame, width=400)
  # # (h, w) = frame.shape[:2]
  # # blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
  # #   0.007843, (300, 300), 127.5)

  # # draw the bounding box around the detected object on
  # # the frame
  # # cv2.rectangle(frame, (startX, startY), (endX, endY),
  # #   (255, 0, 0), 2)

  # # update the new frame in the frame dictionary
  # frameDict[client] = frame

  # # if current time *minus* last time when the active device check
	# # was made is greater than the threshold set then do a check
  # if (datetime.now() - lastActiveCheck).seconds > ACTIVE_CHECK_SECONDS:
	# 	# loop over all previously active devices
  #   for (client, ts) in list(lastActive.items()):
	# 		# remove the RPi from the last active and frame
	# 		# dictionaries if the device hasn't been active recently
  #     if (datetime.now() - ts).seconds > ACTIVE_CHECK_SECONDS:
  #       print("[INFO] lost connection to {}".format(client))
  #       lastActive.pop(client)
  #       frameDict.pop(client)
  #   # set the last active check time as current time
  #   lastActiveCheck = datetime.now()

