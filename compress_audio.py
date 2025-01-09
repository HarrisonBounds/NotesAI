
import os
import sys
from pydub import AudioSegment
from os.path import basename

def compress_mp3_file(mp3_file_path):
    if (not mp3_file_path.endswith(".mp3")): return

    output_file_path = "c_{}.mp3".format(os.path.splitext(basename(mp3_file_path))[0])
    print("\n Processing {} ==> {}".format(mp3_file_path, output_file_path))

    audio_file = AudioSegment.from_file(mp3_file_path, "mp3")
    frame_rate = audio_file.frame_rate
    bytes_per_sample = audio_file.sample_width

    if (frame_rate == 11025):
        print(" frame rate is already 11025, ignore.")
        return

    print(" frame_rate {} ==> {}".format(frame_rate, "11025"))
    audio_file.export(output_file_path, format="mp3", parameters=["-ar", "11025"])

if __name__ == '__main__':
    mp3_file = "audio_files/C++_lecture_2_audio.mp3"

    compress_mp3_file(mp3_file)

    print("\n DONE.")