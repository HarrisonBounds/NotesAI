from openai import OpenAI
import os
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

audio_file= open("audio_files/GreekDramaLecture_EXAMPLE.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)

with open("transcription_files/GreekDramaLectureTranscription_EXAMPLE.txt", "w") as f:
    f.write(transcription.text)
