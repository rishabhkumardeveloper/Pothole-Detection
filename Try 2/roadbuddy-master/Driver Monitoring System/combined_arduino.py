
# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import serial
import requests
try:
        ser = serial.Serial('COM3', 9600)
except:
        pass
def eye_aspect_ratio(eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear
 

# define two constants, one for the eye aspect ratio to indicate
# blink rate and then a second constant for the number of consecutive
# frames the eye must be below the threshold

def alert(timed):
        #ser = serial.Serial('COM3', 9600)
        #ser = serial.Serial('COM3', 9600)

        if (timed==0):
                return time.time()
        else:
                if(time.time()-timed>5):
                        print("alert Eyes on wheel!")
                        try:
                                ser.write(("alert").encode())
                        except:
                                pass

                return timed
                
                        
# loop over frames from the video stream
#while True:
def startfunc():
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 3
    #ser = serial.Serial('COM3', 9600)
    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0
    maxtime=30#constant to set the time for drowsiness detection
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    vs = VideoStream(src=0).start()
    #for raspberry pi uncomment below line
    # vs = VideoStream(usePiCamera=True).start()
    fileStream = False
    time.sleep(1.0)
    timer=0
    eye_cascade = cv2.CascadeClassifier('glasses.xml')
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    color=(0,255,0)
    while(1):
        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = vs.read()
        detect_check=0
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        eyes = eye_cascade.detectMultiScale(frame)
        detect_check=detect_check+len(faces)+len(eyes)
#print(len(faces))
#print(detect_check)
# Display the resulting frame
        for (x,y,w,h) in faces:
        
                 cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
         #roi_gray = gray[y:y+h, x:x+w]
         #roi_color = frame[y:y+h, x:x+w]
        for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        if (detect_check<1):
                timer=alert(timer)
        else:
                timer=0
        #cv2.imshow('frame',frame)
        ##################################################3
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)
        #color=(0,255,0)
        # loop over the face detections
        for rect in rects:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # extract the left and right eye coordinates, then use the
                # coordinates to compute the eye aspect ratio for both eyes
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)

                # average the eye aspect ratio together for both eyes
                ear = (leftEAR + rightEAR) / 2.0

                # compute the convex hull for the left and right eye, then
                # visualize each of the eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, color, 1)
                cv2.drawContours(frame, [rightEyeHull], -1, color, 1)

                if COUNTER>maxtime:
                        print("alert!Wake up")
                        cv2.putText(frame,"Alert! Wake up",(100,100),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        try:
                                ser.write(("alert").encode())
                        except:
                                pass
                color=(0,255,0)
                # check to see if the eye aspect ratio is below the blink
                # threshold, and if so, increment the blink frame counter
                if ear < EYE_AR_THRESH:
                        COUNTER += 1
                        color=(0,0,255)
                        

                # otherwise, the eye aspect ratio is not below the blink
                # threshold
                else:
                        # if the eyes were closed for a sufficient number of
                        # then increment the total number of blinks
                        if COUNTER >= EYE_AR_CONSEC_FRAMES:
                                TOTAL += 1
                                #print("alert")

                        # reset the eye frame counter
                        COUNTER = 0

                # draw the total number of blinks on the frame along with
                # the computed eye aspect ratio for the frame
                cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
 
        # if the `q` key was pressed, break from the loop
        #if key == ord("q"):
                 #       break

startfunc()
# do a bit of cleanup
#cv2.destroyAllWindows()
#vs.stop()
