import argparse
import cv2
import numpy as np


LOWER_YELLOW = np.array([20, 110, 100], dtype=np.uint8)
UPPER_YELLOW = np.array([35, 255, 255], dtype=np.uint8)


def get_yellow_mask(frame_hsv):
    mask = cv2.inRange(frame_hsv, LOWER_YELLOW, UPPER_YELLOW)
    mask = cv2.medianBlur(mask, 7)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return mask


def contour_is_ball(contour):
    area = cv2.contourArea(contour)
    if area < 250:
        return False

    perimeter = cv2.arcLength(contour, True)
    if perimeter <= 0:
        return False

    circularity = 4 * np.pi * area / (perimeter * perimeter)
    if circularity < 0.72:
        return False

    x, y, w, h = cv2.boundingRect(contour)
    if w <= 0 or h <= 0:
        return False

    aspect_ratio = max(w / h, h / w)
    if aspect_ratio > 1.35:
        return False

    extent = area / (w * h)
    if extent < 0.35:
        return False

    return True


def find_ball(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    valid = [contour for contour in contours if contour_is_ball(contour)]
    if not valid:
        return None

    largest = max(valid, key=cv2.contourArea)
    area = cv2.contourArea(largest)
    if area < 250:
        return None

    (x, y), radius = cv2.minEnclosingCircle(largest)
    center = (int(x), int(y))
    radius = int(radius)
    return center, radius, largest


def draw_tracking_info(frame, center, radius, contour):
    cv2.circle(frame, center, radius, (0, 255, 255), 2)
    cv2.circle(frame, center, 3, (0, 255, 255), -1)
    cv2.putText(
        frame,
        "Yellow Ball",
        (center[0] - 40, center[1] - radius - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2,
    )
    cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)


def track_ball(source=0):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video source: {source}")

    cv2.namedWindow("Yellow Ball Tracker", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Yellow Mask", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Yellow Ball Tracker", 640, 480)
    cv2.resizeWindow("Yellow Mask", 640, 480)
    cv2.moveWindow("Yellow Ball Tracker", 100, 100)
    cv2.moveWindow("Yellow Mask", 760, 100)

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = get_yellow_mask(frame_hsv)
        mask = cv2.medianBlur(mask, 7)

        result = find_ball(mask)
        if result is not None:
            center, radius, contour = result
            draw_tracking_info(frame, center, radius, contour)

        cv2.imshow("Yellow Ball Tracker", frame)
        cv2.imshow("Yellow Mask", mask)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="Track a yellow ball with OpenCV")
    parser.add_argument("--video", type=str, default=0, help="Optional path to a video file. Default is your webcam.")
    args = parser.parse_args()

    source = args.video if args.video != "0" else 0
    if str(source).endswith((".mp4", ".avi", ".mov", ".mkv")):
        source = args.video
    track_ball(source)


if __name__ == "__main__":
    main()
