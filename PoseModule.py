import math

import cv2
import mediapipe as mp
import time


class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = True if detectionCon > 0.5 else False
        self.trackCon = True if trackCon > 0.5 else False

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon > 0.5, self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
             for id, lm in enumerate(self.results.pose_landmarks.landmark):
                 h, w, c = img.shape
                 # print(id, lm)
                 cx, cy = int(lm.x*w), int(lm.y * h)
                 self.lmList.append([id, cx, cy])
                 if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0),cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                    math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        return angle

    def finddist(self, img, a1, b2, c3, d4, draw=True):
        first = self.lmList[a1][:2]  # Assuming the landmark list contains (x, y, z) coordinates
        second = self.lmList[b2][:2]
        third = self.lmList[c3][:2]
        fourth = self.lmList[d4][:2]

        left = math.dist(first, second)
        right = math.dist(third, fourth)

        if draw:
            cv2.line(img, tuple(first), tuple(second), (255, 255, 255), 3)
            cv2.putText(img, str(int(left)), tuple(first), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

            cv2.line(img, tuple(third), tuple(fourth), (255, 255, 255), 3)
            cv2.putText(img, str(int(right)), tuple(third), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        return left, right


def main():
    cap = cv2.VideoCapture("videos/model.mp4")
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img)
        print(lmList)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("image :", img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()
