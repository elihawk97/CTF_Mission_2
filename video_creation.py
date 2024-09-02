import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"

from moviepy.editor import *
from pygame import mixer
import numpy as np
from pydub import AudioSegment
from moviepy.editor import TextClip, CompositeVideoClip, VideoClip
from moviepy.video.fx.all import scroll

# Convert WAV to MP3
#sound = AudioSegment.from_wav("spy_music.wav")

#sound.export("spy_music.mp3", format="mp3")

# Load the image
image = ImageClip("star_of_david_image.png").set_duration(5)  # Replace with the actual image filename


# Flickering effect
def flicker(get_frame, t):
    return get_frame(t) * (1 + 0.5 * np.sin(10 * 2 * np.pi * t))

flickering_image = image.fl(flicker)

# Create text animation
txt_clip = TextClip("""MISSION BRIEFING:

                     Muhammad Ismail Darwish (Arabic: محمد إسماعيل درويش),
                     also known as Abu Omar Hassan (Arabic: ابو عمر حس),
                     is a Palestinian politician who has been the 
                     chairman of the Hamas Shura Council since 
                     October 9, 23', succeeding Osama Mazini, after his 
                     killing by Israeli strike."""
                    ,fontsize=24, color='white', font='Courier-New').set_duration(10)
txt_clip = txt_clip.set_position('center').set_start(5).crossfadein(2).crossfadeout(2)

hussan = ImageClip("hussan2.jfif").set_start(19).set_duration(5).resize(5).set_position('center')  # Replace with the actual image filename
hussan = hussan.fl(flicker)

# Create text animation
txt_clip2 = TextClip("""
He is known to use secure servers 
to send critical information via audio to 
fund the infamous Hamas organization. We
believe this data contains key information 
that can lead to his location and elimination.""",
                    fontsize=24, color='white', font='Courier-New').set_duration(10)
txt_clip2 = txt_clip2.set_position('center').set_start(27).crossfadein(2).set_position('center')

# Create text animation
txt_clip3 = TextClip("""
It is believed he uses a LOCAL server 
which is configured to send data through
complex procedures to further destinations.
You must locate the server and retrieve
the files""",
                    fontsize=24, color='white', font='Courier-New').set_duration(10)
txt_clip3 = txt_clip3.set_position('center').set_start(38).crossfadein(2).set_position('center')


# Create text animation
txt_clip4 = TextClip("""
MISSION BRIEFING:

Your objective is to find and eliminate Darwish.
Once his location is located he will be taken out.\n
This operation is critical to national security.\n
The future of the state rests on your shoulders.""",
                    fontsize=24, color='white', font='Courier-New').set_duration(10)
txt_clip4 = txt_clip4.set_position('center').set_start(50).crossfadein(2)

image3 = ImageClip("mossad.jfif").set_start(63).set_duration(5).resize(5).set_position('center')  # Replace with the actual image filename


# Combine image and text
final_video = CompositeVideoClip([flickering_image, txt_clip, hussan, txt_clip2, txt_clip3, txt_clip4, image3])

# Load background music
mixer.init()
mixer.music.load('alert.mp3')  # Replace with your music file
mixer.music.play()

# Write the video file
final_video.write_videofile("spy_mission.mp4", fps=24, codec='libx264', audio='alert.mp3', audio_codec='aac')

mixer.quit()
