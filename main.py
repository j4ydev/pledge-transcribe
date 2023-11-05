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

df = pd.DataFrame(columns=['videoFilePath', 'name', 'transcribe', 'pledge_score'])

listOfDirs = glob.glob("folder*")
listOfDirs.sort()

def transcribe(agentName):
    demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", agentName])
    audioPath = f"separated/mdx_extra/{agentName.split('/')[-1].replace('.mp4', '')}/vocals.mp3"

    options = dict(language="en", beam_size=5, best_of=5)
    transcribeOption = dict(task="transcribe", **options)
    transcription = model.transcribe(audioPath, **transcribeOption)

    transcribedText = transcription["text"]
    return transcribedText

def find_name(transcribedText):
    NER = spacy.load("en_core_web_sm")
    text1= NER(transcribedText)

    name = "not found"
    for word in text1.ents:
        # print(word.text,word.label_)
        if word.label_ == "PERSON":
          name = word.text
    return name


def calculate_sililarity_score(transcribedText):
    actualString = f"pledge to educate myself and others about the potential effects of antimicrobial resistance and help protect tomorrow. Thank you."
    similarityScore = fuzz.partial_ratio(actualString, transcribedText)
    return similarityScore

print("--" * 20)
# for dir in listOfDirs:
dir = "folder_2" #path of the directory
filesList = glob.glob(f"{dir}/*.mp4")
filesList.sort()

print(filesList)

for files in filesList:
    print(files)
    start_time = time.time()
    transcribedText = transcribe(files)
    name = find_name(transcribedText)
    #similarityScore = calculate_sililarity_score(transcribedText)
    
    end_time = time.time()

    calculate_time = end_time - start_time
    
    print("##" * 20)
    ic(transcribedText)
    ic(calculate_time)
    print("##" * 20)

