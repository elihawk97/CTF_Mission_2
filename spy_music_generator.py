import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine

# Function to create a sine wave sound
def create_tone(frequency, duration, volume=-20):
    return Sine(frequency).to_audio_segment(duration=duration).apply_gain(volume)

# Create different tones to mimic spy music
low_tone = create_tone(100, 1000)  # Low, suspenseful tone
high_tone = create_tone(1200, 300) # High-pitched beep

# Combine tones with silence to create a pattern
silence = AudioSegment.silent(duration=200)
pattern = (low_tone + silence + high_tone + silence) * 10  # Repeat pattern

# Add a "heartbeat" effect with bass
bass_beat = create_tone(50, 200).apply_gain(-15)
heartbeat = bass_beat + silence * 2
spy_music = pattern.overlay(heartbeat, loop=True)

# Fade in and out to make it smoother
spy_music = spy_music.fade_in(2000).fade_out(2000)

# Export the audio file
spy_music.export("spy_music.wav", format="wav")

print("Spy music generated and saved as spy_music.wav")
