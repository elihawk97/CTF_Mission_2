import numpy as np
from pydub import AudioSegment
import wave

def binary_to_text(binary_message):
    message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    return message

def extract_message_from_wav(wav_filename):
    with wave.open(wav_filename, 'r') as wav_file:
        frames = wav_file.readframes(wav_file.getnframes())
        samples = np.frombuffer(frames, dtype=np.int16)

    # Extract the binary message from the samples
    binary_message = ''.join(['1' if sample != 0 else '0' for sample in samples[::44100]])
    print(binary_message)
    return binary_to_text(binary_message)

# Example usage
secret_message = extract_message_from_wav('secret_message.wav')
print(f"Secret message: {secret_message}")
