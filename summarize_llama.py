from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

transcription_file = "transcription_files/GreekDramaLectureTranscription_EXAMPLE.txt"
summary_file = "summary_files/GreekDramaLectureNotes_EXAMPLE.txt"

with open(transcription_file, "r") as file:
    text_content = file.read()
    
completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "user",
            "content": f"Please summarize the following text into a concise and organized notes format suitable for studying:\n\n{text_content}"
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

# Open a file to save the output
with open(summary_file, "w") as output_file:
    for chunk in completion:
        # Write each chunk to the file
        content = chunk.choices[0].delta.content or ""
        output_file.write(content)
