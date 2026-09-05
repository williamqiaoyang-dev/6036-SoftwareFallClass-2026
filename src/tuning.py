from os import environ
import cv2, threading, copy

environ["OPENCV_LOG_LEVEL"] = "ERROR"

stop = False
parameters = {
  "gain": 0,
  "exposure": 0,
  "orientation": -100,
  "resolution": "640x480"
}

lastParams = copy.deepcopy(parameters)

def videocap():
  global stop

  cap = cv2.VideoCapture(0)

  cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(parameters['resolution'].split('x')[0]))
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(parameters['resolution'].split('x')[1]))
  cap.set(cv2.CAP_PROP_GAIN, parameters['gain'])
  if parameters['exposure'] == 0:
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
  else:
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    cap.set(cv2.CAP_PROP_EXPOSURE, parameters['exposure'])

  try:
    while cap.isOpened() and not stop:
      for key in parameters.keys():
        if lastParams[key] != parameters[key]:
          lastParams[key] = parameters[key]
          match key:
            case 'resolution':
              cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(parameters['resolution'].split('x')[0]))
              cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(parameters['resolution'].split('x')[1]))
            case 'exposure':
              if parameters['exposure'] == 0:
                cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
              else:
                cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
                cap.set(cv2.CAP_PROP_EXPOSURE, parameters['exposure'])

      ok, frame = cap.read()
      frame = cv2.flip(frame, 1)
      if parameters['orientation'] != -100:
        frame = cv2.rotate(frame, parameters['orientation'])
      if parameters['gain'] != 0:
        frame = cv2.convertScaleAbs(frame, alpha=parameters['gain'], beta=0)

      cv2.imshow("Capture", frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        stop = True
  except KeyboardInterrupt:
    stop = True
  finally:
    cap.release()
    cv2.destroyAllWindows()

def options():
  global stop

  try:
    while not stop:
      ch = input('Enter option: ')
      match ch:
        case 'gain':
          parameters['gain'] = float(input(f"Gain (current {parameters['gain']}): "))
        case 'exposure':
          parameters['exposure'] = float(input(f'Exposure (ms, current {parameters["exposure"]}): '))
        case 'orientation':
          key = parameters['orientation']
          key = '90' if key == cv2.ROTATE_90_CLOCKWISE \
                else '180' if key == cv2.ROTATE_180 \
                else '-90' if key == cv2.ROTATE_90_COUNTERCLOCKWISE \
                else '0'
          key = int(input(f"Degrees (current {key}): "))
          key = round(key / 90) * 90
          key %= 360
          if key < 0: key += 360
          parameters['orientation'] = cv2.ROTATE_90_CLOCKWISE if key == 90 \
                                      else cv2.ROTATE_180 if key == 180 \
                                      else cv2.ROTATE_90_COUNTERCLOCKWISE if key == 270 \
                                      else -100
        case 'resolution':
          parameters['resolution'] = input(f'Resolution (current {parameters["resolution"]}): ')
        case 'clear':
          print('\x1b[2J\x1b[999A\x1b[999D')
        case 'list':
          print(str(parameters))
        case _:
          continue

      print()
  except (KeyboardInterrupt, EOFError):
    stop = True

captureThread = threading.Thread(target=videocap)
captureThread.start()

options()