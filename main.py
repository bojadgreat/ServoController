import math
import cv2
import mediapipe as mp
import serial
import time

# Establish serial connection
ser = serial.Serial('COM5', 9600)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
indexPoint = ()


while True:
    status, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    multiRes = results.multi_hand_landmarks

    if (multiRes):

        for handLms in multiRes:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8:
                    indexPoint = (cx, cy)


        cv2.circle(img, indexPoint, 15, (255, 255, 0), cv2.FILLED)
        print(indexPoint)

        message = f"{indexPoint[0]}\n"
        ser.write(message.encode())

    cv2.imshow("Servo Control", img)
    cv2.waitKey(1)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()
