import os
import subprocess
import customtkinter as ctk
import sounddevice as sd
from scipy.io.wavfile import write
import threading
from pydub import AudioSegment
import numpy as np
from groq import Groq
from os.path import basename

class NotesAIGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NotesAI")
        
        self.root.geometry("600x400")

        self.fs = 44100  # Sample rate
        self.chunk_size = 10
        
        #Retrieve openai api key from environment variable
        api_key = os.getenv("GROQ_API_KEY")

        self.client = Groq(api_key=api_key)

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
        
        self.push_to_github()
        self.cleanup()
    
    def transcribe(self):
        
        audio_file = self.compress_mp3_file(f'audio_files/{self.get_filename("_audio.mp3")}')
        transcription_file = f'transcription_files/{self.get_filename("_transcription.txt")}'
        
        
        with open(audio_file, "rb") as file:
            transcription = self.client.audio.transcriptions.create(
            file=(audio_file, file.read()),
            model="whisper-large-v3",
            response_format="verbose_json",
            )
    
            with open(transcription_file, "w") as output_file:
                output_file.write(transcription.text)
            
        print(f"Transcription saved to {transcription_file}")
        
    def compress_mp3_file(mp3_file_path):
        if (not mp3_file_path.endswith(".mp3")): return

        output_file_path = "{}_compressed.mp3".format(os.path.splitext(basename(mp3_file_path))[0])
        print("\n Processing {} ==> {}".format(mp3_file_path, output_file_path))

        audio_file = AudioSegment.from_file(mp3_file_path, "mp3")
        frame_rate = audio_file.frame_rate
        bytes_per_sample = audio_file.sample_width

        if (frame_rate == 11025):
            print(" frame rate is already 11025, ignore.")
            return

        print(" frame_rate {} ==> {}".format(frame_rate, "11025"))
        audio_file.export(output_file_path, format="mp3", parameters=["-ar", "11025"])
        
        return output_file_path

    def summarize(self):
        transcription_file = f'transcription_files/{self.get_filename("_transcription.txt")}'
        summary_file = f'NOTES/{self.get_filename("_notes.md")}'
        
        with open(transcription_file, "r") as file:
            text_content = file.read()


        # Split the text into two halves
        mid_point = len(text_content) // 2
        first_half = text_content[:mid_point]
        second_half = text_content[mid_point:]

        # Function to send text to model and save output
        def summarize_text(text, output_file):
            completion = self.client.chat.completions.create(
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


        print(f'Summary written to {summary_file}')
        
    def get_filename(self, suffix):
        title = self.get_title()
        if title:
            return f"{title}{suffix}"
        else:
            return f"output{suffix}"

    def get_title(self):
        return self.title_entry.get().strip() or "output"
    
    def push_to_github(self):
        """Push changes to the GitHub repository."""
        try:
            # Change to your repository's root directory
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f'{self.get_filename("_notes.md")} automated update'], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Changes pushed to GitHub successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while pushing to GitHub: {e}")
    
    def cleanup(self):
        os.remove(f'audio_files/{self.get_filename(".wav")}')
        os.remove(f'audio_files/{self.get_filename("_audio.mp3")}')
        os.remove(f'transcription_files/{self.get_filename("_transcription.txt")}')

if __name__ == "__main__":
    root = ctk.CTk()
    app = NotesAIGUI(root)
    root.mainloop()
