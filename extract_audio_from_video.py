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

# TODO:Done Import only needed names or import the module and then use its members. google to know more : JAY
from config import (AUDIO_EXTRACT_CSV_PATH,
                    BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY,
                    BACKGROUND_NOISE_REMOVED_AUDIO_SUB_DIRECTORY,
                    BACKGROUND_REMOVED_FILE_NAME,
                    DIRECTORY_OF_INPUT_VIDEO_DIRECTORY,
                    FAILED_VIDEO_2_AUDIO_CSV_PATH, INPUT_VIDEO_FILE_FORMAT)
from utils import get_metadata_from_file_name, is_value_present_in_dataframe


class VIDEO2AUDIO():
    def __init__(self):
        if os.path.isfile(AUDIO_EXTRACT_CSV_PATH):
            try:
                self.video2audio_dataframe = pd.read_csv(AUDIO_EXTRACT_CSV_PATH)
            except Exception as e:
                print(f"{AUDIO_EXTRACT_CSV_PATH} already present.")
                self.video2audio_dataframe = pd.DataFrame(columns=['video_id', 'extract_audio_time', 'video_duration', 'audio_duration'])
        else:
            self.video2audio_dataframe = pd.DataFrame(columns=['video_id', 'extract_audio_time', 'video_duration', 'audio_duration'])

        if os.path.isfile(FAILED_VIDEO_2_AUDIO_CSV_PATH):
            try:
                self.failed_video2audio_dataframe = pd.read_csv(FAILED_VIDEO_2_AUDIO_CSV_PATH)
            except Exception as e:
                print(f"{FAILED_VIDEO_2_AUDIO_CSV_PATH} already present.")
                self.failed_video2audio_dataframe = pd.DataFrame(columns=['video_id'])
        else:
            self.failed_video2audio_dataframe = pd.DataFrame(columns=['video_id'])

    def add_failed_video2audio_file_to_csv(self, video_path):
        # INSERT DATA IN DATAFRAME

        video_file_name = video_path.split("/")[-1]
        file_bid, file_video_id, file_name_suffix = get_metadata_from_file_name(video_file_name)

        # is_value_present_flag = is_value_present_in_dataframe(file_video_id, self.failed_transcribe_dataframe)
        # if not is_value_present_flag:
        new_failed_video2audio_row = {'video_id': file_video_id}
        new_failed_video2audio_dataframe = pd.DataFrame(new_failed_video2audio_row, index=[0])
        self.failed_video2audio_dataframe = pd.concat([self.failed_video2audio_dataframe, new_failed_video2audio_dataframe], ignore_index=True)
        self.failed_video2audio_dataframe.to_csv(FAILED_VIDEO_2_AUDIO_CSV_PATH, index=False)

    def process(self, input_video_file_list):
        for input_video_path in input_video_file_list:
            video_file_name = input_video_path.split('/')[-1].replace(INPUT_VIDEO_FILE_FORMAT, '')
            file_bid, file_video_id, file_name_suffix = get_metadata_from_file_name(video_file_name)
            is_value_present_flag = is_value_present_in_dataframe(file_video_id, self.video2audio_dataframe)

            # TODO: jay analyse # TODO: Jay i had to do this because the loop was breaking again and again and some exceptions were not getting caught till i added generic exception
            if file_video_id == "6341475570112":
                continue
            if file_video_id == "6341539218112":
                continue
            if file_video_id == "6341599016112":
                continue
            if file_video_id == "6341660118112":
                continue
            if file_video_id == "6341701468112":
                continue
            if file_video_id == "6341703907112":
                continue

            if not is_value_present_flag:
                try:
                    start_time = time.time()
                    demucs.separate.main(["--out", BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY, "--mp3", "--two-stems", "vocals", "-n", "mdx_extra", input_video_path])
                    audio_file_path = f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{BACKGROUND_NOISE_REMOVED_AUDIO_SUB_DIRECTORY}/{video_file_name}/{BACKGROUND_REMOVED_FILE_NAME}"
                    end_time = time.time()
                    extract_audio_time = end_time - start_time

                    clip = VideoFileClip(input_video_path)
                    video_duration = clip.duration
                    audio = AudioSegment.from_file(audio_file_path)
                    audio_duration = len(audio) / 1000  # Convert milliseconds to seconds

                    #RENAME DIRECTORY
                    current_directory = f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{BACKGROUND_NOISE_REMOVED_AUDIO_SUB_DIRECTORY}/{video_file_name}"
                    desired_directory = f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{BACKGROUND_NOISE_REMOVED_AUDIO_SUB_DIRECTORY}/{file_video_id}"
                    shutil.move(current_directory, desired_directory)

                    new_video2audio_row = {'video_id':file_video_id, 'extract_audio_time': extract_audio_time, 'video_duration': video_duration, 'audio_duration': audio_duration}

                    new_video2audio_dataframe = pd.DataFrame(new_video2audio_row, index=[0])
                    self.video2audio_dataframe = pd.concat([self.video2audio_dataframe, new_video2audio_dataframe], ignore_index=True)
                    self.video2audio_dataframe.to_csv(AUDIO_EXTRACT_CSV_PATH, index=False)
                except Exception as e:
                    self.add_failed_video2audio_file_to_csv(input_video_path)
                except: # TODO: Jay i had to do this because the loop was breaking again and again and some exceptions were not getting caught
                    self.add_failed_video2audio_file_to_csv(input_video_path)
            else:
                print(f"Audio of the this {input_video_path} is already seperated.")

if __name__ == "__main__":
    video2audio_obj = VIDEO2AUDIO()
    input_video_folder_list = glob.glob(f"{DIRECTORY_OF_INPUT_VIDEO_DIRECTORY}/*")
    input_video_folder_list.sort()
    start_index = 5
    end_index = 50
    # for input_video_folder in input_video_folder_list:
    for index, input_video_folder in enumerate(input_video_folder_list):
        if start_index <= index and index < end_index:
            input_video_file_list = glob.glob(f"{input_video_folder}/*{INPUT_VIDEO_FILE_FORMAT}")
            input_video_file_list.sort()
            video2audio_obj.process(input_video_file_list)
