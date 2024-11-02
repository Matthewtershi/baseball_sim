import cv2
from moviepy.editor import VideoFileClip
from moviepy.video.fx import speedx

input_video_path = 'pose_videos/1022.mp4'
output_video_path = 'pose_videos/new.mp4'
cap = cv2.VideoCapture(input_video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps  # Duration in seconds
cap.release()

print(f"Frame Rate: {fps}, Duration: {duration} seconds")

adjustment_factor = 4

# Load the video
clip = VideoFileClip(input_video_path)

# Adjust the speed
adjusted_clip = clip.fx(speedx, adjustment_factor)

# Write the output video
adjusted_clip.write_videofile(output_video_path, codec='libx264')
