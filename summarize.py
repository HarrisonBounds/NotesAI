from openai import OpenAI

client = OpenAI(api_key="sk-77paGAPb7KxXOMNm4uT0ZUG-jF3Dq-jAhBFrleOEnDT3BlbkFJGobkdv8QDwjyn6h2l_ZzK-Srms81_pJtQDR7IfjFcA")

with open("transcription.txt", "r") as file:
    text_content = file.read()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Please summarize the following text into a concise and organized notes format suitable for studying:\n\n{text_content}"
        }
    ]
)

summary = completion.choices[0].message.content

with open("summary_notes.txt", "w") as output_file:
    output_file.write(summary)

print("Summary written to summary_notes.txt")