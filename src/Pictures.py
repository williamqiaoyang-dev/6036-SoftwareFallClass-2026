import cv2
import os

os.makedirs("Images", exist_ok=True)
count = 0

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("Camera", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):
        filename = f"Images/frame_{count:05d}.png"
        cv2.imwrite(filename, frame)
        print("Saved to", filename)
        count += 1

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()