# My Solution

import math
import cv2
import numpy as np
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
dir = 0
inc = 0
flag = False

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1288, 720))
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        angle = detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle, (40, 150), (0, 100))
        bar = np.interp(angle, (4e0, 150), (650, 100))


        # Logical Part
        # Check for correct biceps curl
        if 40 < angle < 150:
            print("correct")
            if 80 < per <= 100:
                if dir == 1:
                    count += 0.5
                    dir = 0
            if 0 < per < 30:
                if dir == 0:
                    count += 0.5
                    dir = 1
                    flag = True
        else:
            flag = False  # Set flag to False when correct biceps curl is not detected

        # Check for incorrect movement
        if not(40 < angle < 90) and flag:  # suppose cycle is not over yet and model do approx 50% bicep and fail
            print("incorrect")  # For the Debug Purpose
            if 0 <= per < 30:
                inc += 1
                flag = False  # Reset the flag to prevent multiple increments for a single incorrect movement
        else:
            flag = False
        # Analysis our outcomes
        print(f"count :{count}, incorrect : {inc}, direction : {dir}, percentage : {per}, angle : {angle}, cycle : {flag}")

        cv2.rectangle(img, (1100, 100), (1175, 650), (0, 255, 0), 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 4)

        cv2.putText(img, f"correct : {str(int(count))}", (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.putText(img, f"incorrect : {str(int(inc))}", (50, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("image:", img)
    k = cv2.waitKey(1)
    if k == ord("e") & 0xFF:
        break
cap.release()
cv2.destroyAllWindows()

