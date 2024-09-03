from openai import OpenAI
client = OpenAI(api_key = "sk-77paGAPb7KxXOMNm4uT0ZUG-jF3Dq-jAhBFrleOEnDT3BlbkFJGobkdv8QDwjyn6h2l_ZzK-Srms81_pJtQDR7IfjFcA")

audio_file= open("audio_files/GreekDramaLecture.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)

with open("transciption.txt", "w") as f:
    f.write(transcription.text)