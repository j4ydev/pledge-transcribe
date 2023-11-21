# PART - 0
# util function to read file and extract information ( video_id, batch_index, serial_number, page_number, row, column, nid, bid, file_name_suffix, file_type )

# PART-1.1
# 1. for the INPUT_VIDEO_DIRECTORY loop to extract the audio files,
# 2. save the output in the csv file named output/extract_audio_from_video.csv - having columns -- video_id, extract_audio_time, video_duration, audio_duration
# 3. if the video file that we are processing is already processed - skip re processing
# 4 note: do not keep this  audio_file_path = f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{video_file_name}/vocals.mp3"  instead use
#  audio_file_path = f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{video_id}/vocals.mp3"

# PART-1.2
# NOTE: i somewhere read that the audio can be trimmed if there is no voice in start or end, if this will save the transcribe time we should do it - when we do this add one more column named audio_duration after video_duration

# PART-2
# rename transcribe.py to audio_transcription.py and the input to this process will be BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY
# do generate a o/p csv it will have the following columns -- video_id, transcribe_time, transcribe_text
# skip the files that were previously processed
# output csv file name will be output/audio_transcription.csv

# sequence of execution PART-0, PART-1.1, # PART-2, # PART-1.2

import glob
import os
import shutil
import time

import demucs.separate
import pandas as pd
from icecream import ic
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

# TODO: Import only needed names or import the module and then use its members. google to know more
from config import *
from utils import *


class VIDEO2AUDIO():
    def __init__(self):
        if os.path.isfile(AUDIO_EXTRACT_CSV_PATH):
            try:
                self.video2audio_dataframe = pd.read_csv(AUDIO_EXTRACT_CSV_PATH)
            except:
                self.video2audio_dataframe = pd.DataFrame(columns=['video_id', 'extract_audio_time', 'video_duration', 'audio_duration'])
        else:
            self.video2audio_dataframe = pd.DataFrame(columns=['video_id', 'extract_audio_time', 'video_duration', 'audio_duration'])


    def process(self, input_video_files_list):

        for input_video_path in input_video_files_list:

            clip = VideoFileClip(input_video_path)
            video_file_name = input_video_path.split('/')[-1].replace(INPUT_VIDEO_FILE_FORMAT, '')
            file_video_id, file_name_suffix = get_details_from_video_file_name(video_file_name)
            is_value_present_flag = is_value_present_in_dataframe(file_video_id, self.video2audio_dataframe)

            if not is_value_present_flag:
                start_time = time.time()
                demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", input_video_path])
                audio_file_path = f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{video_file_name}/{BACKGROUND_REMOVED_FILE_NAME}"
                end_time = time.time()
                extract_audio_time = end_time - start_time

                video_duration = clip.duration
                audio = AudioSegment.from_file(audio_file_path)
                audio_duration = len(audio) / 1000  # Convert milliseconds to seconds

                #RENAME DIRECTORY
                os.mkdir(f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{file_video_id}")
                shutil.move(audio_file_path, f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{file_video_id}/{BACKGROUND_REMOVED_FILE_NAME}")
                shutil.rmtree(f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{video_file_name}")

                new_video2audio_row = {'video_id':file_video_id, 'extract_audio_time': extract_audio_time, 'video_duration': video_duration, 'audio_duration': audio_duration}

                new_video2audio_dataframe = pd.DataFrame(new_video2audio_row, index=[0])
                self.video2audio_dataframe = pd.concat([self.video2audio_dataframe, new_video2audio_dataframe], ignore_index=True)
                self.video2audio_dataframe.to_csv(AUDIO_EXTRACT_CSV_PATH, index=False)
            else:
                print(f"Audio of the this {input_video_path} is already seperated.")


if __name__ == "__main__":
    input_video_files_list = glob.glob(f"{ONLY_UNIQUE_VIDEO_DIRECTORY}/*{INPUT_VIDEO_FILE_FORMAT}")
    input_video_files_list.sort()
    video2audio_obj = VIDEO2AUDIO()
    video2audio_obj.process(input_video_files_list)