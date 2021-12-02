# loop over the frames of the video
# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# videoWriter = cv2.VideoWriter('C:/Users/osche/Videos/001.mp4', fourcc, 120.0, (640,480))

args = vars(ap.parse_args())
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
else:
	vs = cv2.VideoCapture(args["video"])

default_trigger = 100
firstFrame = None
Status = False
trigger = 0
avg = None
frameC= 0


memory = None
# while True:
# 	A  = bool(int(input("Letra: ")))
	
def inform(status):
	print("status:", status)

def changed(status, function=print, initial=True):
	global memory
	if status == initial and memory == initial:
		memory = not memory
		function(status)
	elif status is not initial and memory is not initial:
		memory = not(memory)
		function(status)

A, B = np.ones((10,10), dtype="float32")/1, np.ones((5,5), dtype="float32")/1

def refineMask(maskToRefine, kernel_A, kernel_B):
        return cv2.morphologyEx(
               cv2.morphologyEx(maskToRefine, cv2.MORPH_CLOSE, kernel_A),
                                              cv2.MORPH_OPEN,  kernel_B)

class findDiference():
	def __init__(self,diffvalue)  -> None:
		self.avg=None
		self.hasdiffvalue = diffvalue
		pass
	
	def getDiff(self, frame, lock_first=False):
		gray = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (21, 21), 0)

		if lock_first:
			delta = self.getDelta(gray, lock_first, False)
		else:
			_, self.avg = self.getAvarage(gray, self.avg)
			if not _: return not(self.hasdiffvalue), frame
			delta = self.getDelta(gray, self.avg)
		tresh = self.getTreshHold(delta)
		if tresh is None:
			return not(self.hasdiffvalue), frame
		return self.drawContour(frame, self.getContour(tresh))
		


	def getTreshHold(self, frameDelta, _min_limit = 5, a=10, b=5, c=20):
		t, thresh= cv2.threshold(frameDelta, 0,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		if t < _min_limit: return None
		tresh = cv2.morphologyEx(
			refineMask(
				cv2.dilate(thresh, None, iterations=2),
					np.ones((a, a), dtype="float32")/1,
					np.ones((b, b), dtype="float32")/1
			),
			cv2.MORPH_CLOSE,
			cv2.getStructuringElement(
				cv2.MORPH_ELLIPSE, (c, c)
			)
		);
		cv2.imshow("tresh", tresh)
		return tresh 

	def getDelta(self,A, B, avarage=True):
		delta = cv2.absdiff(A, B if not avarage else cv2.convertScaleAbs(B))
		cv2.imshow("delta", delta)
		return delta
	
	def getAvarage(self,gray, save, op=0.1):
		if save is None:
			save = gray.copy().astype("float")
			return False, save

		cv2.accumulateWeighted(gray, save, op)	
		return True, save

	def getContour(self, thresh):
		return imutils.grab_contours(cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE))

	def drawContour(self,img, cnts, _min=100, _max=50000, alpha=0.5):
		frame = img.copy()
		_pass = not(self.hasdiffvalue)
		back = frame.copy()
		for c in cnts:
			if not (_min < cv2.contourArea(c) < _max):
				continue

			cv2.drawContours(frame, [c], -1, (0, 0, 255), 1, cv2.LINE_AA)
			cv2.drawContours(back, [c], -1, (0, 0, 255), -1, cv2.LINE_AA)
			_pass = self.hasdiffvalue	
		return _pass, cv2.addWeighted(frame, 1-alpha, back, alpha, 0)



detectato_status = True
detectado = detectato_status
differ = findDiference(detectato_status)

x,y,w,h = 100, 100, 250, 170

x1,y1,w1,h1 = 50, 50, 400, 300
alpha = 0.5
while True:
	
	status, frame = False, vs.read()
	frame = imutils.resize(frame, width=500, height=500)
	frame = frame if args.get("video", None) is None else frame[1]
	cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
	
	frame_original = frame.copy()
	cv2.rectangle(frame, (x,y), (x+w-2,y+h-2), (0,0,0), -1)
	cv2.rectangle(frame, (x1,y1), (x1+w1,y1+h1), (0,0,0), 2)

	key = cv2.waitKey(1)
	if frame is None or key == ord("q"): break

	back = frame[y:y+h, x:x+w]
	frame = frame[y1:y1+h1, x1:x1+w1]

	status, img = differ.getDiff(frame)
	img = img.copy()
	roi = frame_original[y:y+h, x:x+w]
	roi = cv2.addWeighted(roi, 1-alpha, back, alpha, 0)
	roi = cv2.GaussianBlur(roi, (5,5), 0)
	
	# img[y-y1:y-y1+h, x-x1:x-x1+w] = roi
	frame_original[y1:y1+h1, x1:x1+w1] = img
	frame_original[y:y+h, x:x+w] = roi
	
	img = frame_original
	if status is not detectato_status and trigger > 0:
		trigger-=1
	elif status is detectato_status:
		text, color = "Movimento Detectado", (50, 50,255)
		trigger = default_trigger
		detectado = detectato_status
	else:
		text, color = "Sala limpa", (50,255,50)
		detectado = not(detectato_status)
	
	cv2.putText(img, f"Status: {status} | Timer: {trigger}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
	cv2.putText(img, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

	cv2.imshow("Sensor", img)
	cv2.imshow("Original", frame)
	changed(detectado, inform, detectato_status)
	
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()

		
