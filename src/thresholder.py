import cv2, math

cap = cv2.VideoCapture(0)

while cap.isOpened():
  ok, frame = cap.read()

  labFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

  for i in range(len(frame)):
    for j in range(len(frame[0])):
      if math.dist(labFrame[i][j], (153.55, 130.03, 105.12)) < 2.2:
        frame[i, j] = [0, 0, 255]
        print("E")

  cv2.imshow("Capture", frame)

  if cv2.waitKey(0) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()