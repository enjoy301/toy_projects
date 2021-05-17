import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1)
cap = cv2.VideoCapture(0)
w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
while True:
  success, image = cap.read()
  if not success:
    continue
  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  image.flags.writeable = False
  results = hands.process(image)

  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
      min_x = w - 1;
      max_x = 0.0;
      min_y = h - 1;
      max_y = 0.0
      for i in range(0, 21):  # 요기부터
        hlm = hand_landmarks.landmark[i]
        if hlm.x * w > max_x:
          max_x = hlm.x * w
        if hlm.x * w < min_x:
          min_x = hlm.x * w
        if hlm.y * h > max_y:
          max_y = hlm.y * h
        if hlm.y * h < min_y:
          min_y = hlm.y * h
      image = cv2.rectangle(image, (int(min_x), int(min_y)), (int(max_x), int(max_y)), (0, 0, 0), 2)
  cv2.imshow('input', image)

  if cv2.waitKey(1) == ord('q'):
    break
  if cv2.waitKey(1) == ord('s'):
    cv2.imwrite('files/temp1.png', image)

hands.close()
cap.release()
cv2.destroyAllWindows()