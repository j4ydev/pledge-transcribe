import glob
import os
import time

import numpy as np
import spacy
import whisper
from fuzzywuzzy import fuzz
from icecream import ic

model = whisper.load_model("large")
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
                self.transcribe_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'videoid', 'timeconsumed', 'videoduration', 'transcribetext'])
        else:
            self.transcribe_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'videoid', 'timeconsumed', 'videoduration', 'transcribetext'])

    def transcribe(self, video_file_path):
        # at times incorrect files are also present -- handle this later
        video_file_name = video_file_path.split('/')[-1].replace('.mp4', '')
        demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", video_file_path])
        audioPath = f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{video_file_name}/vocals.mp3"
        options = dict(language="en", beam_size=5, best_of=5)
        transcribe_option = dict(task="transcribe", **options)
        transcription = model.transcribe(audioPath, **transcribe_option, fp16=USE_FP16)
        transcribed_text = transcription["text"]
        return transcribed_text


    def process(self, input_video_files_list):

        for video_file_path in input_video_files_list:
            ic(video_file_path)
            # GET DETAILS OF VIDEO FROM VIDEO FILE NAME
            file_name = video_file_path.split("/")[-1].replace(".mp4","")
            file_row, file_column, file_index, file_pagenumber, file_videoid = get_details_from_video_name(file_name)
            is_value_present_flag = is_value_present_in_dataframe(file_index, self.transcribe_dataframe)

            if not is_value_present_flag:
                # MODULE:1 ------> TRANSCRIBE VIDEO PROCESS
                start_time = time.time()
                file_transcribe_text = self.transcribe(video_file_path)
                end_time = time.time()
                time_consumed = end_time - start_time

                clip = VideoFileClip(video_file_path)
                print( clip.duration )

                # INSERT DATA IN DATAFRAME
                new_transcribe_row = {'row': file_row, 'column': file_column, 'index': file_index, 'pagenumber': file_pagenumber, 'videoid': file_videoid, 'timeconsumed': time_consumed, 'videoduration':clip.duration,  'transcribetext': file_transcribe_text}
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
    input_video_files_list = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*.mp4")
    input_video_files_list.sort()
    transcribe_obj.process(input_video_files_list)
