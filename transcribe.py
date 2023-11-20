import glob
import os
import time

import numpy as np
import spacy
import whisper
from fuzzywuzzy import fuzz

whisper_model = whisper.load_model("large")
import demucs.separate
import pandas as pd
from icecream import ic
from moviepy.editor import VideoFileClip

from config import *
from utils import *


class TRANSCRIBE():
    def __init__(self):
        if os.path.isfile(TRANSCRIBED_FILE_PATH):
            try:
                self.transcribe_dataframe = pd.read_csv(TRANSCRIBED_FILE_PATH)
            except:
                self.transcribe_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'page_number', 'vid', 'extract_audio_time', 'transcribe_time', 'video_duration', 'transcribe_text'])
        else:
            self.transcribe_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'page_number', 'vid', 'extract_audio_time', 'transcribe_time', 'video_duration', 'transcribe_text'])

    def extract_audio_from_mp3(self, video_file_path):
        ## TODO: at times incorrect files are also present -- handle this later
        video_file_name = video_file_path.split('/')[-1].replace(INPUT_VIDEO_FILE_FORMAT, '')
        start_time = time.time()
        demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", video_file_path])
        audio_file_path = f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{video_file_name}/vocals.mp3"
        end_time = time.time()
        extract_audio_time = end_time - start_time
        return extract_audio_time, audio_file_path

    def transcribe_audio(self, audio_file_path):
        start_time = time.time()
        options = dict(language="en", beam_size=5, best_of=5)
        transcribe_option = dict(task="transcribe", **options)
        transcription = whisper_model.transcribe(audio_file_path, **transcribe_option, fp16=USE_FP16)
        transcribed_text = transcription["text"]
        end_time = time.time()
        transcribe_time = end_time - start_time
        return transcribe_time, transcribed_text

    def check_log_and_transcribe_video(self, video_file_path):
        print("--" * 20)
        # GET DETAILS OF VIDEO FROM VIDEO FILE NAME
        file_name = video_file_path.split("/")[-1].replace(INPUT_VIDEO_FILE_FORMAT,"")
        file_row, file_column, file_index, file_pagenumber, file_video_id = get_details_from_video_name(file_name)
        is_value_present_flag = is_value_present_in_dataframe(file_video_id, self.transcribe_dataframe)

        if not is_value_present_flag:
            # MODULE:1 ------> TRANSCRIBE VIDEO PROCESS
            print("processing: ", file_pagenumber, file_index, file_row, file_column, file_video_id, video_file_path)

            clip = VideoFileClip(video_file_path)
            extract_audio_time, audio_file_path = self.extract_audio_from_mp3(video_file_path)
            transcribe_time, file_transcribe_text = self.transcribe_audio(audio_file_path)

            # INSERT DATA IN DATAFRAME
            new_transcribe_row = {'row': file_row, 'column': file_column, 'index': file_index, 'page_number': file_pagenumber, 'vid': file_video_id, 'extract_audio_time': extract_audio_time, 'transcribe_time': transcribe_time, 'video_duration':clip.duration, 'transcribe_text': file_transcribe_text}

            print("##" * 20)
            ic(new_transcribe_row)
            print("##" * 20)

            new_transcribe_dataframe = pd.DataFrame(new_transcribe_row, index=[0])
            self.transcribe_dataframe = pd.concat([self.transcribe_dataframe, new_transcribe_dataframe], ignore_index=True)
            self.transcribe_dataframe.to_csv(TRANSCRIBED_FILE_PATH, index=False)
        else:
            print("Already processed. Skipping: ", file_pagenumber, file_index, file_row, file_column, file_video_id, video_file_path)

    def process(self, input_video_files_list):
        for video_file_path in input_video_files_list:
            try:
                self.check_log_and_transcribe_video(video_file_path)
            except Exception as e:
                ic(e)
                print("FAILED", video_file_path) # TODO: handel this, log it to a separate csv, example 12_2_1_6340799645112_Tapaswini_Bag.mp4'

        return "Complete"

if __name__ == "__main__":
    transcribe_obj = TRANSCRIBE()
    input_video_files_list = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*{INPUT_VIDEO_FILE_FORMAT}")
    input_video_files_list.sort()
    transcribe_obj.process(input_video_files_list)
