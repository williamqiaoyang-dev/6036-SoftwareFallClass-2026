import cv2
import numpy as np

cap = cv2.VideoCapture(0)

targetList = np.tile((46 / 2, 0.4 * 255, 0.65 * 255), (480, 640, 1))

while cap.isOpened():
  ok, frame = cap.read()

  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS).astype(np.float64)
  frame[np.linalg.norm(frame - targetList, axis=-1) < 45] *= [0.06, 1.5, 1]
  frame = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_HLS2BGR)

  cv2.imshow("Capture", frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()