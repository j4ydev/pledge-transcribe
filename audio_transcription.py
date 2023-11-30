import glob
import os
import time

import whisper

whisper_model = whisper.load_model("large")
import pandas as pd
from icecream import ic

from config import (BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY,
                    BACKGROUND_NOISE_REMOVED_AUDIO_SUB_DIRECTORY,
                    BACKGROUND_REMOVED_FILE_NAME, FAILED_TRANSCRIBE_CSV_PATH,
                    TRANSCRIBED_FILE_PATH, USE_FP16)
from utils import is_value_present_in_dataframe, get_metadata_from_file_name

# TODO: Jay: solve in all files Specify an exception class to catch or reraise the exceptionsonarlint(python:S5754)

class TRANSCRIBE():
    def __init__(self):
        if os.path.isfile(TRANSCRIBED_FILE_PATH):
            try:
                self.transcribe_dataframe = pd.read_csv(TRANSCRIBED_FILE_PATH)
            except:
                self.transcribe_dataframe = pd.DataFrame(columns=['video_id', 'transcribe_time', 'transcribe_text'])
        else:
            self.transcribe_dataframe = pd.DataFrame(columns=['video_id', 'transcribe_time', 'transcribe_text'])

        if os.path.isfile(FAILED_TRANSCRIBE_CSV_PATH):
            try:
                self.failed_transcribe_dataframe = pd.read_csv(FAILED_TRANSCRIBE_CSV_PATH)
            except:
                self.failed_transcribe_dataframe = pd.DataFrame(columns=['video_id'])
        else:
            self.failed_transcribe_dataframe = pd.DataFrame(columns=['video_id'])


    def transcribe_audio(self, audio_file_path):
        start_time = time.time()
        options = dict(language="en", beam_size=5, best_of=5)
        transcribe_option = dict(task="transcribe", **options)
        transcription = whisper_model.transcribe(audio_file_path, **transcribe_option, fp16=USE_FP16)
        transcribed_text = transcription["text"]
        end_time = time.time()
        transcribe_time = end_time - start_time
        return transcribe_time, transcribed_text

    def check_log_and_transcribe_video(self, audio_directory_path):
        file_video_id = audio_directory_path.split("/")[-1]
        is_value_present_flag = is_value_present_in_dataframe(file_video_id, self.transcribe_dataframe)
        audio_file_path = f"{audio_directory_path}/{BACKGROUND_REMOVED_FILE_NAME}"
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

    def add_failed_transcribe_file_to_csv(self, audio_path):
        # INSERT DATA IN DATAFRAME
        audio_file_name = audio_path.split("/")[-1]
        file_bid, file_video_id, file_name_suffix = get_metadata_from_file_name(audio_file_name)

        # is_value_present_flag = is_value_present_in_dataframe(file_video_id, self.failed_transcribe_dataframe)
        # if not is_value_present_flag:
        new_failed_transcribe_row = {'video_id': file_video_id}
        new_failed_transcribe_dataframe = pd.DataFrame(new_failed_transcribe_row, index=[0])
        self.failed_transcribe_dataframe = pd.concat([self.failed_transcribe_dataframe, new_failed_transcribe_dataframe], ignore_index=True)
        self.failed_transcribe_dataframe.to_csv(FAILED_TRANSCRIBE_CSV_PATH, index=False)


    def process(self, audio_directory_list):
        for audio_directory_path in audio_directory_list:
            try:
                self.check_log_and_transcribe_video(audio_directory_path)
            except Exception as e:
                ic(e)
                print("FAILED", audio_directory_path)
                self.add_failed_transcribe_file_to_csv(audio_directory_path)
        return "Complete"

if __name__ == "__main__":
    transcribe_obj = TRANSCRIBE()
    audio_directory_list = glob.glob(f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{BACKGROUND_NOISE_REMOVED_AUDIO_SUB_DIRECTORY}/*")
    audio_directory_list.sort()
    transcribe_obj.process(audio_directory_list)

