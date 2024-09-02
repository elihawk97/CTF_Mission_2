import yt_dlp
from moviepy.editor import VideoFileClip
import os

# Function to download video from YouTube using yt-dlp
def download_video(youtube_url, output_path="video.mp4"):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print(f"Video downloaded: {output_path}")
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
    return output_path

# Function to extract audio from video
def extract_audio(video_path, audio_output_path="audio.mp3"):
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_output_path)
        audio_clip.close()
        video_clip.close()
        print(f"Audio extracted: {audio_output_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")

if __name__ == "__main__":
    # Example YouTube URL
    youtube_url = "https://www.youtube.com/watch?v=oW1jQ-zh6zY"

    # Download video
    video_file = download_video(youtube_url)

    if video_file:
        # Extract audio
        extract_audio(video_file)

        # Optionally, remove the video file
        os.remove(video_file)
        print(f"Video file {video_file} deleted.")
