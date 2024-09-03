import sounddevice as sd
from scipy.io.wavfile import write

# Parameters
fs = 44100  # Sample rate
seconds = 5  # Duration of recording

print("Recording...")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
print("Finished recording.")

# Save as WAV file
write('output.wav', fs, myrecording)