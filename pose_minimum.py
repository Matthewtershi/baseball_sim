import cv2 # type: ignore
import mediapipe as mp # type: ignore
import time

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

print("test")
cap = cv2.VideoCapture("pose_videos/1102.mp4")
previousTime = 0
finalw = 1280
finalh = 720
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # for color compatibility
    results = pose.process(imgRGB)
    
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, landmark in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            print(id, landmark)
            cx, cy = landmark.x * w, landmark.y * h # converting landmark so that its relative to width and heigh
            print(cx, cy)
            cv2.circle(img, (int(cx), int(cy)), 10, (255, 0, 0), cv2.FILLED) 

    currTime = time.time()
    fps = 1/(currTime-previousTime)
    previousTime = currTime

    cv2.putText(img, str(fps), (70,50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    resized_img = cv2.resize(img, (finalw,finalh))
    cv2.imshow("Image", resized_img)
    cv2.waitKey(1)
