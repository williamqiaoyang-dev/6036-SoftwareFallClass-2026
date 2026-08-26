import cv2 # adds a module (more utility code) to your program

cap = cv2.VideoCapture(0) # usually, 0 is the index of your webcam
while cap.isOpened(): # while the camera is running
    ok, frame = cap.read() # ok stores whether it succeeded
    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()