from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

transcription_file = "transcription_files/C++_lecture_2_transcription.txt"
summary_file = "NOTES/C++_lecture_2_notes.md"

# Read the transcription file
with open(transcription_file, "r") as file:
    text_content = file.read()

# Split the text into two halves
mid_point = len(text_content) // 2
first_half = text_content[:mid_point]
second_half = text_content[mid_point:]

# Function to send text to model and save output
def summarize_text(text, output_file):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": f"Please summarize the following text into a concise and organized notes format suitable for studying:\n\n{text}"
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Append each chunk's output to the file
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        output_file.write(content)

# Open the summary file to append the output
with open(summary_file, "w") as output_file:
    # Summarize the first half and append
    summarize_text(first_half, output_file)
    output_file.write("\n\n---\n\n")  # Optional separator
    # Summarize the second half and append
    summarize_text(second_half, output_file)
