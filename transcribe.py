from openai import OpenAI
client = OpenAI(api_key = "your_api_key")

audio_file= open("audio_files/GreekDramaLecture.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)

with open("transciption.txt", "w") as f:
    f.write(transcription.text)
