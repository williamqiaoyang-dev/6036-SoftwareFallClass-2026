import numpy as np
import cv2, glob

size = (9, 6)
objp = np.zeros((1, size[0] * size[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:size[0], 0:size[1]].T.reshape(-1, 2)

objectPoints, imagePoints = [], []
images = glob.glob('Images/*.png')
imageSize = None
for filename in images:
  img = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2GRAY) # type: ignore
  imageSize = img.shape[::-1]
  ok, corners = cv2.findChessboardCorners(img, size, None)
  if ok:
    # for corner in corners:
      # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
      # corners = cv2.cornerSubPix(img, corners, (11, 11), (-1, -1), criteria)
      # cv2.drawChessboardCorners(img, size, corners, ok)
    objectPoints.append(objp)
    imagePoints.append(corners)
  cv2.imwrite("I" + filename, img)

ok, matrix, dist, rvecs, tvecs = cv2.calibrateCamera(objectPoints, imagePoints, imageSize, None, None) # type: ignore

np.savez('calib.npz', mtx=matrix, dist=dist)