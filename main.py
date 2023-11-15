import glob
import time

import numpy as np
import spacy
import whisper
from fuzzywuzzy import fuzz
from icecream import ic

model = whisper.load_model("large")
import demucs.separate
import pandas as pd

BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY = "separated/mdx_extra"
TRANSCRIBED_FILE_PATH = "output/transcribe_text.csv" ### PATH OF THE OUTPUT CSV FILE
INPUT_VIDEO_DIRECTORY = "/Users/jay/work/pledge-transcribe_/new_video" ### DIRECTORY OF VIDEO FILES (DO NOT ADD / AT THE END OF THE PATH)

class TRANSCRIBE():
    def __init__(self):
        self.df = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'videoid', 'timeconsumed', 'transcribetext'])

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

    def process(self, dir_path, csv_path):
        dir = dir_path
        filesPathList = glob.glob(f"{dir}/*.mp4")
        filesPathList.sort()
        print(filesPathList)

        for filePath in filesPathList:
            print(filePath)
            # transcribe text

            start_time = time.time()
            transcribedText = self.transcribe(filePath)
            end_time = time.time()
            time_consumed = end_time - start_time


            file_name = filePath.split("/")[-1].replace(".mp4","")
            file_name_separate_list = file_name.split("_")
            file_row = file_name_separate_list[1]
            file_column = file_name_separate_list[2]
            file_index = 4*(file_row) + file_column
            file_pagenumber = file_name_separate_list[0]
            file_videoid = file_name_separate_list[3]
            file_transcribetext = transcribedText

            #update database
            new_row = {
            'row': file_row,
            'column': file_column,
            'index': file_index,
            'pagenumber': file_pagenumber,
            'videoid': file_videoid,
            'timeconsumed': time_consumed,
            'transcribetext': file_transcribetext
            }

            print("##" * 20)
            ic(new_row)
            print("##" * 20)

            new_df = pd.DataFrame(new_row, index=[0])
            self.df = pd.concat([self.df, new_df], ignore_index=True)

            # Save the DataFrame as a CSV file            
            self.df.to_csv(csv_path, index=False)


####
if __name__ == "__main__":
    dir = INPUT_VIDEO_DIRECTORY
    csv_path = TRANSCRIBED_FILE_PATH
    transcribe_obj = TRANSCRIBE()
    transcribe_obj.process(dir, csv_path)