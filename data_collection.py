import os
from pytube import YouTube
from moviepy.editor import VideoFileClip

output_folder = "pose_videos"
os.makedirs(output_folder, exist_ok=True)

video_urls = [
    "https://www.youtube.com/watch?v=example1",
    "https://www.youtube.com/watch?v=example2",
]

target_length = 12

def download_and_adjust_video(url, output_folder, target_length):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(file_extension="mp4").get_highest_resolution()
        video_path = video_stream.download(output_path=output_folder)
        
        # Load the downloaded video with moviepy
        video_clip = VideoFileClip(video_path)
        original_duration = video_clip.duration

        # Calculate speed factor to reach target duration
        speed_factor = original_duration / target_length

        # Adjust video speed
        adjusted_clip = video_clip.fx(lambda clip: clip.speedx(factor=speed_factor))
        
        # Save adjusted video
        adjusted_video_path = os.path.join(output_folder, f"{yt.video_id}_adjusted.mp4")
        adjusted_clip.write_videofile(adjusted_video_path, codec="libx264")

        os.remove(video_path)
        print(f"Downloaded and adjusted: {yt.title}")
        
    except Exception as e:
        print(f"Failed to process video {url}: {e}")

for url in video_urls:
    download_and_adjust_video(url, output_folder, target_length)
