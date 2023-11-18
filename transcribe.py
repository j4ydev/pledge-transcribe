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
from config import *
from utils import *

class TRANSCRIBE():
    def __init__(self):
        if os.path.isfile(TRANSCRIBED_FILE_PATH):
            try:
                self.transcribeDataframe = pd.read_csv(TRANSCRIBED_FILE_PATH)
            except:
                self.transcribeDataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'videoid', 'timeconsumed', 'transcribetext'])
        else:
            self.transcribeDataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'videoid', 'timeconsumed', 'transcribetext'])

    def transcribe(self, videoFilePath):
        # at times incorrect files are also present -- handle this later
        videoFileName = videoFilePath.split('/')[-1].replace('.mp4', '')
        demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", videoFilePath])
        audioPath = f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{videoFileName}/vocals.mp3"
        options = dict(language="en", beam_size=5, best_of=5)
        transcribeOption = dict(task="transcribe", **options)
        transcription = model.transcribe(audioPath, **transcribeOption)
        transcribedText = transcription["text"]
        return transcribedText


    def process(self, inputVideoFilesList):

        for videoFilePath in inputVideoFilesList:
            ic(videoFilePath)
            # GET DETAILS OF VIDEO FROM VIDEO FILE NAME
            file_name = videoFilePath.split("/")[-1].replace(".mp4","")
            file_row, file_column, file_index, file_pagenumber, file_videoid = get_details_from_video_name(file_name)
            is_value_present_flag = is_value_present_in_dataframe(file_index, self.transcribeDataframe)

            if not is_value_present_flag:
                # MODULE:1 ------> TRANSCRIBE VIDEO PROCESS
                start_time = time.time()
                fileTranscribeText = self.transcribe(videoFilePath)
                end_time = time.time()
                time_consumed = end_time - start_time

                # INSERT DATA IN DATAFRAME
                newTranscribeRow = {'row': file_row, 'column': file_column, 'index': file_index, 'pagenumber': file_pagenumber, 'videoid': file_videoid, 'timeconsumed': time_consumed, 'transcribetext': fileTranscribeText}
                print("##" * 20)
                ic(newTranscribeRow)
                print("##" * 20)
                newTranscribeDF = pd.DataFrame(newTranscribeRow, index=[0])
                self.transcribeDataframe = pd.concat([self.transcribeDataframe, newTranscribeDF], ignore_index=True)
                # Save the DataFrame as a CSV file
                self.transcribeDataframe.to_csv(TRANSCRIBED_FILE_PATH, index=False)
            else:
                print("DATA ALREADY PRESENT IN DATAFRAME.")
        return "Complete"

if __name__ == "__main__":
    transcribe_obj = TRANSCRIBE()
    inputVideoFilesList = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*.mp4")
    inputVideoFilesList.sort()
    transcribe_obj.process(inputVideoFilesList)
