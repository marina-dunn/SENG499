# import the necessary packages
import imagezmq
import argparse
import socket
import time
import cv2
import msgpack
import numpy as np
import glob

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
  help="ip address of the server to which the client will connect")
ap.add_argument("-p", "--server-port", required=True,
  help="port of the server to which the client will connect")
ap.add_argument("-a", "--action", required=True,
  help="action to train")

args = vars(ap.parse_args())

# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to=f'tcp://{args["server_ip"]}:{args["server_port"]}')
print("ImageSender connected")

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
host = socket.gethostname()

gestures = ['smile', 'neutral', 'frown']

print(args['action'])

results = {}
for filename in glob.glob(f'client/media/identified_gestures/{gestures[int(args["action"])]}/*'):
  image = cv2.imread(filename)
  reply = sender.send_image(host, image)
  reply = msgpack.unpackb(reply)
  data = reply['faces']
  if len(data) > 0:
    result = data[0]["result"]
    if result not in results:
      results[result] = 0
    results[result] += 1

print(results)