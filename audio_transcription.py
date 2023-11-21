import glob
import os
import time

import whisper

whisper_model = whisper.load_model("large")
import pandas as pd
from icecream import ic

from config import *
from utils import *


class TRANSCRIBE():
    def __init__(self):
        if os.path.isfile(TRANSCRIBED_FILE_PATH):
            try:
                self.transcribe_dataframe = pd.read_csv(TRANSCRIBED_FILE_PATH)
            except:
                self.transcribe_dataframe = pd.DataFrame(columns=['video_id', 'transcribe_time', 'transcribe_text'])
        else:
            self.transcribe_dataframe = pd.DataFrame(columns=['video_id', 'transcribe_time', 'transcribe_text'])

    def transcribe_audio(self, audio_file_path):
        start_time = time.time()
        options = dict(language="en", beam_size=5, best_of=5)
        transcribe_option = dict(task="transcribe", **options)
        transcription = whisper_model.transcribe(audio_file_path, **transcribe_option, fp16=USE_FP16)
        transcribed_text = transcription["text"]
        end_time = time.time()
        transcribe_time = end_time - start_time
        return transcribe_time, transcribed_text

    def check_log_and_transcribe_video(self,audio_folder_path):

        audio_folder_path_name = audio_folder_path.split("/")[-1]
        file_video_id = audio_folder_path_name
        is_value_present_flag = is_value_present_in_dataframe(file_video_id, self.transcribe_dataframe)
        audio_file_path = f"{audio_folder_path}/{BACKGROUD_REMOVED_FILE_NAME}"
        ic(audio_file_path)

        if not is_value_present_flag:
            # MODULE:1 ------> TRANSCRIBE VIDEO PROCESS
            print("processing: ",  audio_file_path)
            transcribe_time, file_transcribe_text = self.transcribe_audio(audio_file_path)

            # INSERT DATA IN DATAFRAME
            new_transcribe_row = {'video_id': file_video_id, 'transcribe_time': transcribe_time, 'transcribe_text': file_transcribe_text}

            print("##" * 20)
            ic(new_transcribe_row)
            print("##" * 20)

            new_transcribe_dataframe = pd.DataFrame(new_transcribe_row, index=[0])
            self.transcribe_dataframe = pd.concat([self.transcribe_dataframe, new_transcribe_dataframe], ignore_index=True)
            self.transcribe_dataframe.to_csv(TRANSCRIBED_FILE_PATH, index=False)


    def process(self, audio_folder_list):

        for audio_folder_path in audio_folder_list:
            try:
                self.check_log_and_transcribe_video(audio_folder_path)
            except Exception as e:
                ic(e)
                print("FAILED", audio_folder_path) # TODO: handel this, log it to a separate csv, example 12_2_1_6340799645112_Tapaswini_Bag.mp4'

        return "Complete"
if __name__ == "__main__":
    transcribe_obj = TRANSCRIBE()
    audio_folder_list = glob.glob(f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/*")
    audio_folder_list.sort()
    transcribe_obj.process(audio_folder_list)
