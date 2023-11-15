import glob
import time
import whisper
import numpy as np
import spacy
from fuzzywuzzy import fuzz
from icecream import ic
model = whisper.load_model("large")
import demucs.separate

import pandas as pd

class TRANSCRIBE():
    def __init__(self):
        self.df = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'videoid', 'transcribetext'])

    def transcribe(self, agentName):
        demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", agentName])
        audioPath = f"separated/mdx_extra/{agentName.split('/')[-1].replace('.mp4', '')}/vocals.mp3"

        options = dict(language="en", beam_size=5, best_of=5)
        transcribeOption = dict(task="transcribe", **options)
        transcription = model.transcribe(audioPath, **transcribeOption)

        transcribedText = transcription["text"]

        return transcribedText

    def process(self, dir_path, csv_path):
        dir = dir_path 
        filesList = glob.glob(f"{dir}/*.mp4")
        filesList.sort()
        print(filesList)

        for files in filesList:
            print(files)
            # transcribe text

            start_time = time.time()
            transcribedText = self.transcribe(files)
            end_time = time.time()
            calculate_time = end_time - start_time

            print("##" * 20)
            ic(transcribedText)
            ic(calculate_time)
            print("##" * 20)


            file_name = files.split("/")[-1].replace(".mp4","")
            file_name_seperate_list = file_name.split("_")
            file_row = file_name_seperate_list[1]
            file_column = file_name_seperate_list[2]
            file_index = "index_number"
            file_pagenumber = file_name_seperate_list[0]
            file_videoid = file_name_seperate_list[3]
            file_transcribetext = transcribedText

            #update database
            new_row = {
            'row': file_row, 
            'column': file_column,
            'index': file_index,
            'pagenumber': file_pagenumber,
            'videoid': file_videoid, 
            'transcribetext': file_transcribetext
            }

            new_df = pd.DataFrame(new_row, index=[0])
            self.df = pd.concat([self.df, new_df], ignore_index=True)

        # Save the DataFrame as a CSV file
        self.df.to_csv(csv_path, index=False)


####
if __name__ == "__main__":
    dir = "/Users/jay/work/pledge-transcribe_/new_video" ### DIRECTORY OF VIDEO FILES (DO NOT ADD / AT THE END OF THE PATH)
    csv_path = "transcribe_text.csv" ### PATH OF THE CSV FILE
    transcribe_obj = TRANSCRIBE()
    transcribe_obj.process(dir, csv_path)