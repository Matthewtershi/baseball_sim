import cv2 # type: ignore
import mediapipe as mp # type: ignore
import time

# static_image_mode=False,
# model_complexity=1,
# smooth_landmarks=True,
# enable_segmentation=False,
# smooth_segmentation=True,
# min_detection_confidence=0.5,
# min_tracking_confidence=0.5):

class poseDetector():
    
    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()

    def __init__(self, mode=False, complex=1, smooth_land=True, upBody = False, smooth_seg = True, detectionCon = 0.5, trackingCon = 0.5):
        self.mode = mode
        self.complexity = complex
        self.smooth_land = smooth_land
        self.upBody = upBody
        self.smooth_seg = smooth_seg
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth_land, self.upBody, self.smooth_seg, self.detectionCon, self.trackingCon)

    def findPose(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # for color compatibility
        self.results = self.pose.process(imgRGB)
    
        # print(results.pose_landmarks)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img
    
    def findPosition(self, img, draw=True):
        lmList = []
        if self.results.pose_landmarks:
            for id, landmark in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, landmark)
                cx, cy = landmark.x * w, landmark.y * h # converting landmark so that its relative to width and heigh
                # print(cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (int(cx), int(cy)), 10, (255, 0, 0), cv2.FILLED) 
        return lmList

def main():
    cap = cv2.VideoCapture("pose_videos/1022.mp4")
    previousTime = 0
    finalw = 1280
    finalh = 720
    detector = poseDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img) # coordinates of 33 landmarks
        print(lmList)

        currTime = time.time()
        fps = 1/(currTime-previousTime)
        previousTime = currTime

        cv2.putText(img, str(fps), (70,50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        resized_img = cv2.resize(img, (finalw,finalh))
        cv2.imshow("Image", resized_img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()