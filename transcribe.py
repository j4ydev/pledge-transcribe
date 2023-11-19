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
                self.transcribe_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'vid', 'timeconsumed', 'videoduration', 'transcribetext'])
        else:
            self.transcribe_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'vid', 'timeconsumed', 'videoduration', 'transcribetext'])

    def transcribe_video(self, video_file_path):
        ## TODO: at times incorrect files are also present -- handle this later
        video_file_name = video_file_path.split('/')[-1].replace(INPUT_VIDEO_FILE_FORMAT, '')
        demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", video_file_path])
        audio_path = f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{video_file_name}/vocals.mp3"
        options = dict(language="en", beam_size=5, best_of=5)
        transcribe_option = dict(task="transcribe", **options)
        transcription = whisper_model.transcribe(audio_path, **transcribe_option, fp16=USE_FP16)
        transcribed_text = transcription["text"]
        return transcribed_text


    def process(self, input_video_files_list):

        for video_file_path in input_video_files_list:
            ic(video_file_path)
            # GET DETAILS OF VIDEO FROM VIDEO FILE NAME
            file_name = video_file_path.split("/")[-1].replace(INPUT_VIDEO_FILE_FORMAT,"")
            file_row, file_column, file_index, file_pagenumber, file_video_id = get_details_from_video_name(file_name)
            print(file_video_id)
            is_value_present_flag = is_value_present_in_dataframe(file_video_id, self.transcribe_dataframe)

            if not is_value_present_flag:
                # MODULE:1 ------> TRANSCRIBE VIDEO PROCESS
                start_time = time.time()
                file_transcribe_text = self.transcribe_video(video_file_path)
                end_time = time.time()
                time_consumed = end_time - start_time
                clip = VideoFileClip(video_file_path)

                # INSERT DATA IN DATAFRAME
                new_transcribe_row = {'row': file_row, 'column': file_column, 'index': file_index, 'pagenumber': file_pagenumber, 'vid': file_video_id, 'timeconsumed': time_consumed, 'videoduration':clip.duration,  'transcribetext': file_transcribe_text}
                print("##" * 20)
                ic(new_transcribe_row)
                print("##" * 20)
                new_transcribe_dataframe = pd.DataFrame(new_transcribe_row, index=[0])
                self.transcribe_dataframe = pd.concat([self.transcribe_dataframe, new_transcribe_dataframe], ignore_index=True)
                # Save the DataFrame as a CSV file
                self.transcribe_dataframe.to_csv(TRANSCRIBED_FILE_PATH, index=False)
            else:
                print("DATA ALREADY PRESENT IN DATAFRAME.")
        return "Complete"

if __name__ == "__main__":
    transcribe_obj = TRANSCRIBE()
    input_video_files_list = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*{INPUT_VIDEO_FILE_FORMAT}")
    input_video_files_list.sort()
    transcribe_obj.process(input_video_files_list)
