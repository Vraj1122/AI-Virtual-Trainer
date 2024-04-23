# Chatgpt's Solution

import cv2
import numpy as np
import PoseModule as pm
cap = cv2.VideoCapture("videos/trial.mp4")
detector = pm.poseDetector()
bicep_curl_count = 0

# Constants for the elbow movement detection
ELBOW_DOWN = 0
ELBOW_UP = 1
WAIT_FOR_DOWN = 2

prev_elbow_position = None
elbow_state = ELBOW_DOWN

while True:
    success, img = cap.read()
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        shoulder = lmList[11]
        elbow = lmList[13]
        wrist = lmList[15]

        # Estimate bicep curl based on elbow movement
        if wrist[1] == shoulder[1]:
            if elbow_state == ELBOW_DOWN:
                # Detected upward movement of the elbow
                elbow_state = ELBOW_UP
        else:
            if elbow_state == ELBOW_UP:
                # Detected downward movement of the elbow after an up movement
                bicep_curl_count += 1
                elbow_state = WAIT_FOR_DOWN
            elif elbow_state == WAIT_FOR_DOWN:
                # Waiting for the elbow to go back down before counting another curl
                elbow_state = ELBOW_DOWN

        print(f"Bicep Curl Count: {bicep_curl_count}")

        cv2.putText(img, f"Bicep Curl Count: {str(int(bicep_curl_count))}", (50, 100), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 0), 3)

    cv2.imshow("image:", img)
    k = cv2.waitKey(1)
    if k == ord("e") & 0xFF:
        break

cap.release()
cv2.destroyAllWindows()
