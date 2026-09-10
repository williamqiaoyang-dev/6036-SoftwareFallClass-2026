import numpy as np
import cv2

with np.load('calib.npz') as calibration:
  cmatrix = calibration['mtx']
  dcoeffs = calibration['dist']
  print(calibration)
  print(cmatrix)

h, w = 480, 640
newmat, roi = cv2.getOptimalNewCameraMatrix(cmatrix, dcoeffs, (w, h), alpha=0)
x, y, wb, hb = roi

cap = cv2.VideoCapture(0)

while cap.isOpened():
  ok, frame = cap.read()

  frame = cv2.undistort(frame, cmatrix, dcoeffs, None, newmat)[y:y+hb, x:x+wb]

  cv2.imshow("Capture", frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
