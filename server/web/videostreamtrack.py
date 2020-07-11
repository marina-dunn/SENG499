# import the necessary packages
from threading import Thread
import asyncio

class VideoStreamTrack:
  def __init__(self, track, name="VideoStreamTrack"):
		# initialize the video camera stream and read the first frame
		# from the stream
    self.track = track

		# initialize the thread name
    self.name = name

		# initialize the variable used to indicate if the thread should
		# be stopped
    self.stopped = False

  def start(self):
		# start the thread to read frames from the video stream
    t = Thread(target=self.update, name=self.name, args=())
    t.daemon = True
    t.start()
    return self

  async def update(self):
		# keep looping infinitely until the thread is stopped
    while True:
			# if the thread indicator variable is set, stop the thread
      if self.stopped:
        return

			# otherwise, read the next frame from the stream
      self.frame = await self.track.recv()

  def read(self):
		# return the frame most recently read
    return self.frame

  def stop(self):
		# indicate that the thread should be stopped
    self.stopped = True