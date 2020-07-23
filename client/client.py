# import the necessary packages
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time
import cv2
import msgpack
import numpy as np

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
  help="ip address of the server to which the client will connect")
ap.add_argument("-p", "--server-port", required=True,
  help="port of the server to which the client will connect")
args = vars(ap.parse_args())

# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to=f'tcp://{args["server_ip"]}:{args["server_port"]}')
print("ImageSender connected")

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
host = socket.gethostname()
# vs = VideoStream(usePiCamera=True).start()
vs = VideoStream(src=0).start()
time.sleep(2.0) # Let camera warm up

start = time.time()
frame_count = 0
 
while True:
	# read the frame from the camera and send it to the server
  frame = vs.read()
  if vs.grabbed:
    # frame = imutils.resize(frame, width=320) # Resize frame if needed
    reply = sender.send_image(host, frame)
    frame_count = frame_count+1
    (h, w) = frame.shape[:2]
    if reply:
      data = msgpack.unpackb(reply)
      elapsed_time = time.time() - start
      fps = frame_count/elapsed_time
      cv2.putText(frame, f'FPS: {fps}', (10, 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255,0), 2)
      cv2.putText(frame, f'Time: {elapsed_time}', (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255,0), 2)
      cv2.putText(frame, f'Frames: {frame_count}', (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255,0), 2)
      cv2.putText(frame, f'found {len(data)} faces', (10, h - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255,0), 2)
                
      keypoints = []
      for face in data:
        for facial_feature in face['features']:
          keypoints.extend([cv2.KeyPoint(x[0], x[1], 4) for x in face['features'][facial_feature]])
          
      im_with_keypoints = cv2.drawKeypoints(frame,
                                              keypoints,
                                              np.array([]),
                                              (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
      cv2.imshow('Client',im_with_keypoints)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
  
cv2.destroyAllWindows()