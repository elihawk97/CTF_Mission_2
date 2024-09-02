import numpy as np
from scipy.io.wavfile import write

# Parameters
sample_rate = 44100  # Sample rate in Hz
duration = 10  # Duration in seconds

# Generate a time array
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Create a mysterious sound using a combination of low-frequency sine waves and random noise
freq1 = 130.81  # C3
freq2 = 164.81  # E3
freq3 = 196.00  # G3

# Generate sine waves
sine_wave1 = 0.3 * np.sin(2 * np.pi * freq1 * t)
sine_wave2 = 0.3 * np.sin(2 * np.pi * freq2 * t)
sine_wave3 = 0.3 * np.sin(2 * np.pi * freq3 * t)

# Combine sine waves
music = sine_wave1 + sine_wave2 + sine_wave3

# Add some random noise
noise = 0.05 * np.random.normal(0, 1, music.shape)
music += noise

# Normalize to the range of 16-bit PCM
music = np.int16(music / np.max(np.abs(music)) * 32767)

# Write to WAV file
write('mysterious_music.wav', sample_rate, music)

print('WAV file saved as mysterious_music.wav')
