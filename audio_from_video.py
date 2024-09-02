from pydub import AudioSegment
import subprocess

def convert_video_to_wav_ffmpeg(video_file, output_wav):
    try:
        # Use ffmpeg to extract audio from video
        temp_audio_file = "temp_audio.mp3"
        subprocess.run([
            "ffmpeg",
            "-i", video_file,
            "-q:a", "0",
            "-map", "a",
            temp_audio_file
        ], check=True)

        # Convert the extracted audio to WAV using pydub
        audio = AudioSegment.from_file(temp_audio_file, format="mp3")
        audio.export(output_wav, format="wav")

        print(f"Audio has been successfully saved as: {output_wav}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during ffmpeg processing: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # File paths
    video_file = "video.f251.webm"  # Replace with your video file name
    output_wav = "output_audio.wav"  # Desired output file name

    # Convert the video to WAV
    convert_video_to_wav_ffmpeg(video_file, output_wav)
