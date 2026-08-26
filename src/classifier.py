import cv2

cap = cv2.VideoCapture(0)

classifiers = {
  "Face": cv2.CascadeClassifier("C:/Users/accel/AppData/Local/Programs/Python/Python311/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
}

while cap.isOpened():
  ok, frame = cap.read()

  for name, classifier in classifiers.items():
    rects = classifier.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=5)
    for (x, y, w, h) in rects:
      cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 5)
      cv2.putText(frame, name, (x + 2, y - 7), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

  cv2.imshow("Capture", frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()