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
- [OpenAI Python Client](https://github.com/openai/openai-python)
- [FFmpeg](https://ffmpeg.org/) (required by PyDub for audio conversion)

## Cloning the Repository

To clone the repository, run the following command in your terminal:

w
git clone https://github.com/your-username/repository-name.git
w

Replace `your-username/repository-name` with the actual path of the repository you want to clone.


## Installation

1. Install the required Python packages:

   ```
   pip install customtkinter sounddevice scipy pydub openai
   ```

2. Install FFmpeg:

   - **Windows**: Download from [FFmpeg's website](https://ffmpeg.org/download.html) and add it to the system PATH.
   - **MacOS**: Install using Homebrew:
     ```
     brew install ffmpeg
     ```
   - **Linux**: Install using your package manager, e.g., `sudo apt install ffmpeg`.

3. Set up your OpenAI API key:

   - Sign up at [OpenAI](https://platform.openai.com/signup) and create an API key. NOTE: Depending on which model you use, OpenAI does ask for payment per token. 
   - Set the environment variable `OPENAI_API_KEY`:
     ```
     export OPENAI_API_KEY='your-api-key'
     ```
     Replace `'your-api-key'` with your actual OpenAI API key.

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

4. All generated files (audio recordings, transcriptions, and summaries) will be saved in organized directories within the project folder:

   - `audio_files/`: Contains recorded audio files in `.wav` and `.mp3` formats.
   - `transcription_files/`: Contains transcription files in `.txt` format.
   - `summary_files/`: Contains summarized notes in `.txt` format.

## Code Structure

- **`NotesAIGUI` class**: The main class for the GUI and handling core functionalities.
  - **`start_recording()`**: Starts audio recording.
  - **`stop_recording()`**: Stops audio recording.
  - **`record()`**: Records audio in chunks and saves it as a `.wav` file, then converts it to `.mp3`.
  - **`transcribe_and_summarize()`**: Handles transcription and summarization.
  - **`transcribe()`**: Uses OpenAI's Whisper model to transcribe audio.
  - **`summarize()`**: Uses OpenAI's GPT model to summarize the transcribed text.
  - **`get_filename()`**: Generates filenames based on the provided title or defaults.
  - **`cleanup()`**: Cleans up temporary audio files.

## Dependencies

The application depends on the following Python libraries:

- `customtkinter`: For creating a modern and customizable GUI.
- `sounddevice`: For audio recording.
- `scipy`: For handling audio file formats.
- `pydub`: For converting between audio formats.
- `openai`: For interacting with OpenAI's API.

## Troubleshooting

- **Audio Recording Issues**: Ensure your microphone is properly connected and recognized by the system.
- **FFmpeg Not Found**: Make sure FFmpeg is installed and added to your system PATH.
- **API Key Errors**: Verify that your OpenAI API key is set correctly as an environment variable.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

- Thanks to [OpenAI](https://openai.com/) for providing robust APIs for transcription and text summarization.
- Thanks to the developers of [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for creating a modern and customizable Tkinter framework.

## Contact

For questions or suggestions, please contact [your-email@example.com](mailto:your-email@example.com).
