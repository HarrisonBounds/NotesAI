# NotesAI

NotesAI is a desktop application that allows users to record audio, transcribe it, and summarize the transcription into organized notes suitable for studying. This application leverages OpenAI's API for transcription and summarization, providing a streamlined solution for turning recorded lectures, meetings, or any audio into concise notes.

## Features

- **Record Audio**: Record audio directly from the GUI.
- **Transcribe Audio**: Automatically transcribe recorded audio into text using OpenAI's Whisper model.
- **Summarize Transcription**: Summarize the transcribed text into a study-friendly notes format using OpenAI's GPT model.
- **Save Files**: Save recorded audio, transcriptions, and summaries to organized files for easy access.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7+
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [SoundDevice](https://python-sounddevice.readthedocs.io/)
- [SciPy](https://www.scipy.org/)
- [PyDub](https://github.com/jiaaro/pydub)
- [Groq Python Client](https://github.com/groq/groq-python)
- [FFmpeg](https://ffmpeg.org/) (required by PyDub for audio conversion)

## Cloning the Repository

To clone the repository, run the following command in your terminal:

```
git clone https://github.com/HarrisonBoundsNotesAI.git
```

## Installation

1. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

2. Install FFmpeg:

   - **Windows**: Download from [FFmpeg's website](https://ffmpeg.org/download.html) and add it to the system PATH.
   - **MacOS**: Install using Homebrew:
     ```
     brew install ffmpeg
     ```
   - **Linux**: Install using your package manager, e.g., `sudo apt install ffmpeg`.

3. Set up your Groq API key:

   - Sign up at [Groq](https://console.groq.com/) and create an API key.
   - Set the environment variable `GROQ_API_KEY`:
     ```
     export GROQ_API_KEY='your-api-key'
     ```
     Replace `'your-api-key'` with your actual OpenAI API key.

4. Install Git

- **Windows**: Download Git from [Git's official website](https://git-scm.com/download/win) and follow the installation prompts.
- **macOS**: Install using Homebrew:
  
  ```
  brew install git
  ```
- **Linux**: Install using your package manager. For example, on Debian/Ubuntu:
   ```
  sudo apt install git
  ```

## Usage

1. Run the application:

   ```
   python notesai.py
   ```

2. The GUI will open, providing the following options:

   - **Notes Title**: Enter a title for your notes.
   - **Record Button**: Click to start recording audio.
   - **Stop Button**: Click to stop recording.

3. After stopping the recording, the application will automatically transcribe the audio and summarize the transcription into a notes format.

4. All generated files (audio recordings, transcriptions) will be deleted after the summary is complete. The summary will then be autoamtically pushed to your repository in the NOTES folder. 

## Code Structure

- **`NotesAIGUI` class**: The main class for the GUI and handling core functionalities.
  - **`start_recording()`**: Starts audio recording.
  - **`stop_recording()`**: Stops audio recording.
  - **`record()`**: Records audio in chunks and saves it as a `.wav` file, then converts it to `.mp3`.
  - **`transcribe_and_summarize()`**: Handles transcription and summarization.
  - **`transcribe()`**: Uses OpenAI's Whisper model to transcribe audio.
  - **`summarize()`**: Uses Meta's Llama3 model to summarize the transcribed text.
  - **`get_filename()`**: Generates filenames based on the provided title or defaults.
  - **`cleanup()`**: Cleans up temporary audio files.

## Dependencies

The application depends on the following Python libraries:

- `customtkinter`: For creating a modern and customizable GUI.
- `sounddevice`: For audio recording.
- `scipy`: For handling audio file formats.
- `pydub`: For converting between audio formats.
- `groq`: For interacting with Groq's API.

## Troubleshooting

- **Audio Recording Issues**: Ensure your microphone is properly connected and recognized by the system.
- **FFmpeg Not Found**: Make sure FFmpeg is installed and added to your system PATH.
- **API Key Errors**: Verify that your Groq API key is set correctly as an environment variable.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.


## Contact

For questions or suggestions, please contact [harrison.bounds777@gmail.com](mailto:harrison.bounds777@gmail.com).
