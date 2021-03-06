import cv2
import sys
import os
import time
import math
import numpy as np
from sys import platform
import argparse
from imutils.video import VideoStream

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + '/python/openpose/Release')
os.environ['PATH'] = os.environ['PATH'] + ';' + \
  dir_path + '/Release;' + dir_path + '/bin;'

import pyopenpose as op

def set_params():
  params = dict()
  params["logging_level"] = 3
  params["output_resolution"] = "-1x-1"
  params["net_resolution"] = "-1x368"
  params["model_pose"] = "BODY_25"
  params["alpha_pose"] = 0.6
  params["scale_gap"] = 0.3
  params["scale_number"] = 1
  params["render_threshold"] = 0.05
  params["num_gpu_start"] = 0
  params["disable_blending"] = False
  params["model_folder"] = dir_path + '/models'
  return params


def main():
  params = set_params()

  opWrapper = op.WrapperPython()
  opWrapper.configure(params)
  opWrapper.start()

  webcam = VideoStream(src=0).start()

  font = cv2.FONT_HERSHEY_SIMPLEX

  while True:
    frame = webcam.read()
    frame = cv2.resize(frame, (400, 300))
    datum = op.Datum()
    datum.cvInputData = frame
    opWrapper.emplaceAndPop([datum])

    # cam = datum.cvOutputData
    cam = frame

    # print(type(datum.poseKeypoints))
    # print(isinstance(datum.poseKeypoints, np.ndarray))
    # print(datum.poseKeypoints.size)

    # if (type(datum.poseKeypoints) == )

    # nose position
    if (isinstance(datum.poseKeypoints, np.ndarray) 
      and datum.poseKeypoints.size == 75):
        noseX = datum.poseKeypoints[0][0][0]
        noseY = datum.poseKeypoints[0][0][1]
        cv2.circle(cam, (noseX, noseY), 5, (0, 255, 255))

        neckX = datum.poseKeypoints[0][1][0]
        neckY = datum.poseKeypoints[0][1][1]
        cv2.circle(cam, (neckX, neckY), 5, (0, 255, 255))

        rWristX = datum.poseKeypoints[0][4][0]
        rWristY = datum.poseKeypoints[0][4][1]
        cv2.circle(cam, (rWristX, rWristY), 5, (0, 255, 255))

        right_hand_up(cam, (noseX, noseY), (neckX, neckY), (rWristX, rWristY))

        lWristX = datum.poseKeypoints[0][7][0]
        lWristY = datum.poseKeypoints[0][7][1]
        cv2.circle(cam, (lWristX, lWristY), 5, (0, 255, 255))

        left_hand_up(cam, (noseX, noseY), (neckX, neckY), (lWristX, lWristY))

    # noseX = datum.poseKeypoints[0][0][0]
    # noseY = datum.poseKeypoints[0][0][1]
    # cv2.circle(cam, (noseX, noseY), 5, (0, 255, 255))
    # kPoints = datum.poseKeypoints[0, i, :, :]

    # Display the stream
    # cv2.resize(cam, (256, 144))
    cv2.imshow('Est', cam)

    # keyboard interactions
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

  cv2.destroyAllWindows()

def right_hand_up(cam, nose, neck, wrist):
  nose_neck = (nose[1]-neck[1])/(nose[0]-neck[0])
  neck_wrist = (neck[1]-wrist[1])/(neck[0]-wrist[0])
  cv2.line(cam, nose, neck, (0, 0, 0), 1)
  cv2.line(cam, neck, wrist, (0, 0, 0), 1)

  angle = np.arctan(abs((nose_neck - neck_wrist)/(1 + nose_neck*neck_wrist))) * 180 / np.pi
  # cv2.putText(cam, "r_angle: " + str(angle), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
  #     (0, 0, 0), 1)
  if (angle < 100 and angle > 80):
    cv2.putText(cam, "r_TRUE", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    (0, 0, 0), 1)
  else:
    cv2.putText(cam, "r_FALSE", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    (0, 0, 0), 1)

def left_hand_up(cam, nose, neck, wrist):
  nose_neck = (nose[1]-neck[1])/(nose[0]-neck[0])
  neck_wrist = (neck[1]-wrist[1])/(neck[0]-wrist[0])
  cv2.line(cam, nose, neck, (0, 0, 0), 1)
  cv2.line(cam, neck, wrist, (0, 0, 0), 1)

  angle = np.arctan(abs((nose_neck - neck_wrist)/(1 + nose_neck*neck_wrist))) * 180 / np.pi
  # cv2.putText(cam, "l_angle: " + str(angle), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
  #     (0, 0, 0), 1)
  if (angle < 100 and angle > 80):
    cv2.putText(cam, "l_TRUE", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    (0, 0, 0), 1)
  else:
    cv2.putText(cam, "l_FALSE", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    (0, 0, 0), 1)
  

if __name__ == '__main__':
    main()


# trained model method - way too slow

# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--prototxt", required=True,
#                 help="path to Caffe 'deploy' prototxt file")
# ap.add_argument("-m", "--model", required=True,
#                 help="path to Caffe pre-trained model")
# ap.add_argument("-c", "--confidence", type=float, default=0.5,
#                 help="minimum probability to filter weak detections")
# args = vars(ap.parse_args())

# protoFile = "/pose_deploy_linevec_faster_4_stages.prototxt"
# weightsFile = "/pose_iter_160000.caffemodel"
# imageFile = "/genji.png"
# npoints = 15
# POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]

# # net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
# net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# # this frame can be passed in from camera feed
# frame = cv2.imread(dir_path + imageFile)
# frameWidth = frame.shape[1]
# frameHeight = frame.shape[0]
# threshold = 0.1

# inWidth = 300
# inHeight = 300

# blob = cv2.dnn.blobFromImage(
#     cv2.resize(frame, (300, 300)), 1.0 / 255, (inWidth, inHeight),
#     (104.0, 177.0, 123.0), swapRB=False, crop=False)

# net.setInput(blob)
# output = net.forward()

# H = output.shape[2]
# W = output.shape[3]
# points = []

# for i in range(npoints):
#     probMap = output[0, i, :, :]
#     minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
#     x = (frameWidth * point[0]) / W
#     y = (frameHeight * point[1]) / H

#     if prob > threshold :
#         cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
#         cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 3, lineType=cv2.LINE_AA)
#         points.append((int(x), int(y)))
#     else:
#         points.append(None)

# for pair in POSE_PAIRS:
#     partA = pair[0]
#     partB = pair[1]

#     if points[partA] and points[partB]:
#         cv2.line(frame, points[partA], points[partB], (0, 255, 255), 2)
#         cv2.circle(frame, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

# cv2.imshow("Output", frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
