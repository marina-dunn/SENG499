import cv2
import numpy as np
import imagezmq
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import ssl
import msgpack
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
  help="ip address of the server to which the client will connect")
ap.add_argument("-p", "--server-port", required=True,
  help="port of the server to which the client will connect")
args = vars(ap.parse_args())

def sendImageToServer(frame):
    # When we have incoming request, create a receiver and subscribe to a publisher

    decoded = cv2.imdecode(np.frombuffer(frame, np.uint8), -1)

    sender = imagezmq.ImageSender(connect_to=f'tcp://{args["server_ip"]}:{args["server_port"]}')
    reply = sender.send_image('Web', decoded)
    (h, w) = decoded.shape[:2]
    if reply:
      result = msgpack.unpackb(reply)
      print(result)
      data = result['faces']
      # cv2.putText(decoded, f'found {len(data)} faces', (10, h - 20),
      #   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255,0), 2)
                
      # keypoints = []
      # for face in data:
      #   for facial_feature in face['features']:
      #     keypoints.extend([cv2.KeyPoint(x[0], x[1], 4) for x in face['features'][facial_feature]])
          
      # im_with_keypoints = cv2.drawKeypoints(decoded,
      #                                         keypoints,
      #                                         np.array([]),
      #                                         (0, 0, 255),
      #                                         cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
      # jpg = cv2.imencode('.jpg', im_with_keypoints)[1]               
      # cv2.imshow('Test', im_with_keypoints)   
      # cv2.waitKey(0)
      # cv2.destroyAllWindows()   
      print (f'Found {len(data)} Faces')
      if len(result['error']) > 0:
        yield b'Error: ' + bytes(result['error'], 'utf-8')
      elif len(data) != 1:
        yield b'Error: Need one face'  
      else:  
        action = data[0]['result']  
        print (f'Result: {action}') 
        yield bytes(action, 'utf-8')
    else:
      print('No Reply')
      yield b'No Reply'
    # while True:
    #   # Pull an image from the queue
    #   camName, frame = receiver.recv_image()
    #   # Using OpenCV library create a JPEG image from the frame we have received
    #   jpg = cv2.imencode('.jpg', frame)[1]
    #   # Convert this JPEG image into a binary string that we can send to the browser via HTTP
    #   yield b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'+jpg.tostring()+b'\r\n'

# Add `application` method to Request class and define this method here
@Request.application
def application(request):
    # What we do is we `sendImagesToWeb` as Iterator (generator) and create a Response object
    # based on its output.
    print('Request recieved')
    if request.method == "POST":
        if request.files:
            image = request.files["photo"].read()
            return Response(sendImageToServer(image), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response('Hello')

if __name__ == '__main__':
    # This code starts simple HTTP server that listens on interface localhost, port 4000
    # This is an internal service only
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.check_hostname = False
    ssl_context.load_cert_chain('localhost.crt', 'localhost_decrypted.key')
    run_simple('127.0.0.1', 4000, application, ssl_context=ssl_context, threaded=True)