import os
import customtkinter as ctk
import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
import threading
from pydub import AudioSegment
import numpy as np

class NotesAIGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NotesAI")
        
        self.root.geometry("600x400")

        self.fs = 44100  # Sample rate
        self.chunk_size = 30
        
        #Retrieve openai api key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")

        self.client = OpenAI(api_key=api_key)

        self.recording = False
        self.recorded_chunks = []  # Store recorded audio chunks
        
        # Create text entry for note title
        self.title_label = ctk.CTkLabel(root, text="Notes Title:")
        self.title_label.pack(pady=10)

        self.title_entry = ctk.CTkEntry(root, placeholder_text="Enter title here")
        self.title_entry.pack(pady=10)

        # Create buttons
        self.record_button = ctk.CTkButton(root, text="Record", command=self.start_recording)
        self.record_button.pack(pady=20)

        self.stop_button = ctk.CTkButton(root, text="Stop", command=self.stop_recording, state="disabled")
        self.stop_button.pack(pady=20)
        

    def start_recording(self):
        self.recording = True
        self.record_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        self.record_thread = threading.Thread(target=self.record)
        self.record_thread.start()

    def stop_recording(self):
        self.recording = False
        self.stop_button.configure(state="disabled")

    def record(self):
        print("Recording...")
        while self.recording:
            chunk = sd.rec(int(self.fs * self.chunk_size), samplerate=self.fs, channels=1)
            sd.wait()  # Wait until the recording is finished
            self.recorded_chunks.append(chunk)  # Append chunk to the list

        print("Finished recording.")
        
        # Concatenate all chunks
        full_recording = np.concatenate(self.recorded_chunks, axis=0)
        
        # Save the final recording
        wav_filename = f'audio_files/{self.get_filename(".wav")}'
        write(wav_filename, self.fs, full_recording)
        
        # Convert to mp3
        sound = AudioSegment.from_wav(wav_filename)
        sound.export(f'audio_files/{self.get_filename("_audio.mp3")}', format="mp3")
        
        # Clear the recorded chunks list for the next recording
        self.recorded_chunks.clear()

        self.transcribe_and_summarize()

    def transcribe_and_summarize(self):
        print("Transcribing Audio")
        self.transcribe()
        print("Summarizing Transcription")
        self.summarize()
    
    def transcribe(self):
        
        print("Here")
        audio_file= open(f'audio_files/{self.get_filename("_audio.mp3")}', "rb")
        transcription_file = f'transcription_files/{self.get_filename("_transcription.txt")}'
        
        
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
            
        print("Here1")
        
        with open(transcription_file, "w") as f:
            f.write(transcription.text)
            
        print(f"Transcription saved to {transcription_file}")

    def summarize(self):
        transcription_file = f'transcription_files/{self.get_filename("_transcription.txt")}'
        summary_file = f'summary_files/{self.get_filename("_notes.txt")}'
        with open(transcription_file, "r") as file:
            text_content = file.read()

        completion = self.client.chat.completions.create(
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

        with open(summary_file, "w") as output_file:
            output_file.write(summary)

        print(f'Summary written to {summary_file}')
        
    def get_filename(self, suffix):
        title = self.get_title()
        if title:
            return f"{title}{suffix}"
        else:
            return f"output{suffix}"

    def get_title(self):
        return self.title_entry.get().strip() or "output"
    
    def cleanup(self):
        os.remove(f'audio_files/{self.get_filename(".wav")}')

if __name__ == "__main__":
    root = ctk.CTk()
    app = NotesAIGUI(root)
    root.mainloop()
