from ultralytics import YOLO # type: ignore
import cv2

cap = cv2.VideoCapture(0)
count = 0

model = YOLO("../runs/detect/train-2/weights/best.pt")

while cap.isOpened():
  ok, frame = cap.read()

  results = model(frame)[0]
  for result in results:
    xyxy = result.boxes.xyxy.int().tolist()
    conf = result.boxes.conf.tolist()
    for i in range(len(conf)):
      # if conf[i] > 0.5:
        cv2.rectangle(frame, xyxy[i][:2], xyxy[i][2:], (255, 255, 255), 1)
        cv2.putText(frame, f"Ball ({conf[i] * 100:.1f}%)", xyxy[i][:2], cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255))

  cv2.imshow("Capture", frame)

  match cv2.waitKey(1) & 0xFF:
    case 32:
      cv2.imwrite(f"./src/images/{count:05d}.jpg", frame)
      count += 1
    case 113:
      break

cap.release()
cv2.destroyAllWindows()