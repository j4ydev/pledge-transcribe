import glob
import os
import time

import cv2
import numpy as np
import pandas as pd
from capture_face_img import GETFRAME
from deepface.commons import distance as dst
from deepface.commons import functions, realtime
from face_embedding import FACEEMBEDDINGS
from icecream import ic
from video_transcribe import TRANSCRIBE

transcribe_obj = TRANSCRIBE()
getframe_obj = GETFRAME()
faceembeddings_obj = FACEEMBEDDINGS()

### ALL PATHS WILL BE DEFINED HERE ###
# TODO: move "separated/mdx_extra" -> "output/separated/mdx_extra"
BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY = "separated/mdx_extra"
TRANSCRIBED_FILE_PATH = "output/transcribe_text.csv" ### PATH OF THE OUTPUT CSV FILE
FACE_MATCH_RESULT_CSV_PATH = "output/face_match.csv"
INPUT_VIDEO_DIRECTORY = "/Users/jay/work/new_video" ### DIRECTORY OF VIDEO FILES (DO NOT ADD / AT THE END OF THE PATH)
FACE_IMAGE_DIRECTORY = "output/screenshots" # PATH DIR OF SAVE FRAME FROM VIDEO (DO NOT ADD / AT THE END OF PATH)
FACE_IMAGE_INDEX_DIRECTORY = "output/image_index" # PATH DIR OF SAVE FACE EMBEDDINGS FROM SCREENSHOTS (DO NOT ADD / AT THE END OF THE PATH)

### IF TRANSCRIBE DATAFRAME EXIST OR NOT EXISTS ###
if os.path.isfile(TRANSCRIBED_FILE_PATH):
    try:
        transcribe_dataframe = pd.read_csv(TRANSCRIBED_FILE_PATH)
    except:
        transcribe_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'vid', 'extract_audio_time', 'transcribe_time', 'transcribetext'])
else:
    transcribe_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'vid', 'extract_audio_time', 'transcribe_time', 'transcribetext'])

### IF FACEMATCHING DATAFRAME EXIST OR NOT EXISTS ###
if os.path.isfile(FACE_MATCH_RESULT_CSV_PATH):
    try:
        face_match_dataframe = pd.read_csv(FACE_MATCH_RESULT_CSV_PATH)
    except:
        face_match_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'video-id_1', 'similarity_score_1','video-id_2','similarity_score_2', 'video-id_3','similarity_score_3'])
else:
    face_match_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'vid', 'match_videoid_1', 'similarity_score_1','match_videoid_2','similarity_score_2', 'match_videoid_3','similarity_score_3'])

### GET DETAILS FROM VIDEO FILE NAME ###
def get_details_from_video_name(file_name):
    file_name_separate_list = file_name.split("_")
    file_row = file_name_separate_list[1]
    file_column = file_name_separate_list[2]
    file_index = 4*(int(file_row)-1) + int(file_column)
    file_pagenumber = file_name_separate_list[0]
    file_video_id = file_name_separate_list[3]

    return file_row, file_column, file_index, file_pagenumber, file_video_id

### CHECK IF VIDEO IS ALREADY PROCESSED OR NOT ###
def is_value_present(index_number, dataframe):
    if index_number in dataframe["index"].values:
        return True
    else:
        return False

### CHECK IF SCREENSHOT ALREADY PRESENT IN DIRECTORY ###
def check_if_screenshot_present(imageFileName):
    possible_screenshot_path = f"{FACE_IMAGE_DIRECTORY}/{imageFileName}"
    if os.path.isfile(possible_screenshot_path):
        return True
    else:
        return False

### CAPTURE IMAGE WHICH CONTAIN FACE ###
### RECURRENT THE FUNCTION UNTIL YOU GET FACE IMAGE ###
def capture_face_image_and_embedding(videoFilePath, imageFileName):
    frame = getframe_obj.getImageFromVideo(videoFilePath)
    frameFilePath = f'{FACE_IMAGE_DIRECTORY}/{imageFileName}'
    # Save the frame as an image
    print(frameFilePath)
    print("--")
    cv2.imwrite(frameFilePath, frame)

    embeddingData = faceembeddings_obj.find_face_embedding(frameFilePath)
    if embeddingData == "face not detected" or embeddingData == "None":
        embeddingData = capture_face_image_and_embedding(videoFilePath, imageFileName)
    else:
        pass
    return embeddingData

### GET 2 CLOSEST FACES AND THEIR SCORE FROM DIRECTORY. ###
def find_videoid_and_score(first_two_pairs):
    first_two_pairs = dict(first_two_pairs)
    first_distance = True
    for distance in first_two_pairs:
        print("aaaa",first_two_pairs[distance])
        file_row, file_column, file_index, file_pagenumber, file_video_id = get_details_from_video_name(first_two_pairs[distance].split("/")[-1].replace(".mp4",""))
        if first_distance:
            first_distance = False
            videoid_1 = file_video_id
            similarity_score_1 = 1 - float(distance)
            ic(videoid_1)
            print("@@"* 50)
        else:
            videoid_2 = file_video_id
            similarity_score_2 = 1 - float(distance)
    return videoid_1, similarity_score_1, videoid_2, similarity_score_2

### MAIN LOOP ###
def process(transcribe_dataframe, face_match_dataframe):
    inputVideoFilesList = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*.mp4")
    inputVideoFilesList.sort()

    for videoFilePath in inputVideoFilesList:
        ic(videoFilePath)

        embeddingFilesList = glob.glob(f"{FACE_IMAGE_INDEX_DIRECTORY}/*.txt")
        embeddingFilesList.sort()

        # GET DETAILS OF VIDEO FROM VIDEO FILE NAME
        file_name = videoFilePath.split("/")[-1].replace(".mp4","")
        file_row, file_column, file_index, file_pagenumber, file_video_id = get_details_from_video_name(file_name)
        is_value_present_flag = is_value_present(file_index, transcribe_dataframe)

        if not is_value_present_flag:
            # MODULE:1 ------> TRANSCRIBE VIDEO PROCESS
            start_time = time.time()
            fileTranscribeText = transcribe_obj.transcribe(videoFilePath)
            end_time = time.time()
            time_consumed = end_time - start_time
            # # TODO: This will break re-write the file
            # INSERT DATA IN DATAFRAME
            newTranscribeRow = {'row': file_row, 'column': file_column, 'index': file_index, 'pagenumber': file_pagenumber, 'vid': file_video_id, 'transcribe_time': time_consumed, 'transcribetext': fileTranscribeText}
            print("##" * 20)
            ic(newTranscribeRow)
            print("##" * 20)
            newTranscribeDF = pd.DataFrame(newTranscribeRow, index=[0])
            transcribe_dataframe = pd.concat([transcribe_dataframe, newTranscribeDF], ignore_index=True)

            # Save the DataFrame as a CSV file
            transcribe_dataframe.to_csv(TRANSCRIBED_FILE_PATH, index=False)
        else:
            print("DATA ALREADY PRESENT IN DATAFRAME.")


        # is_value_present_flag = is_value_present(file_index, embeding_dataframe)
        # MODULE:2 ------> CAPTURE FACE IMAGES
        imageFileName = videoFilePath.split("/")[-1].replace(".mp4", ".png")
        screenshot_present_flag = check_if_screenshot_present(imageFileName)
        if not screenshot_present_flag:

            # MODULE:3 ------> SAVE IMAGE EMBEDDINGS
            embeddingData = capture_face_image_and_embedding(videoFilePath, imageFileName)
            ### create image_index file
            imageIndexFileName = videoFilePath.split("/")[-1].replace(".mp4", ".txt")
            imageIndexFilePath = f"{FACE_IMAGE_INDEX_DIRECTORY}/{imageIndexFileName}"

            with open(imageIndexFilePath, 'w') as f:
                f.write(str(embeddingData))

    faceEmbeddingList = glob.glob(f"{FACE_IMAGE_INDEX_DIRECTORY}/*.txt")
    faceEmbeddingList.sort()

    for faceEmbeddingPath in faceEmbeddingList:
        # MODULE:4 ------> COMPARE IMAGE WITH OTHER IMAGES
        embeddingFileName = faceEmbeddingPath.split("/")[-1].replace(".txt","")
        file_row, file_column, file_index, file_pagenumber, file_video_id = get_details_from_video_name(embeddingFileName)
        is_face_embedding_present_flag = is_value_present(file_index, face_match_dataframe)
        similar_face_score_dict = {}
        if not is_face_embedding_present_flag:
            with open(faceEmbeddingPath, "r") as f:
                current_image_embedding = f.read()
            current_image_embedding = eval(current_image_embedding)


            for embedding_path in embeddingFilesList:
                print(embedding_path)
                with open(embedding_path, "r") as f:
                    image_from_dir = f.read()
                print("::" * 20)

                image_from_dir = eval(image_from_dir)

                a = np.matmul(np.transpose(np.array(image_from_dir[0]["embedding"])), np.array(current_image_embedding[0]["embedding"]))
                b = np.sum(np.multiply(np.array(image_from_dir[0]["embedding"]), np.array(image_from_dir[0]["embedding"])))
                c = np.sum(np.multiply(np.array(current_image_embedding[0]["embedding"]), np.array(current_image_embedding[0]["embedding"])))

                distance = 1 - (a / (np.sqrt(b) * np.sqrt(c)))

                similar_face_score_dict[str(distance)] = embedding_path
            sorted_dict = dict(sorted(similar_face_score_dict.items()))

            if len(sorted_dict) > 2:
                first_two_pairs = list(sorted_dict.items())[:2]
            else:
                first_two_pairs = list(sorted_dict.items())[:len(sorted_dict)]

            print(first_two_pairs)
            videoid_1, similarity_score_1, videoid_2, similarity_score_2 = find_videoid_and_score(first_two_pairs)

            # INSERT DATA IN DATAFRAME
            newFaceRow = {'row': file_row, 'column': file_column, 'index': file_index, 'pagenumber': file_pagenumber, 'vid': file_video_id, 'match_videoid_1': file_video_id, 'similarity_score_1': 1,'match_videoid_2': videoid_1, 'similarity_score_2': similarity_score_1, 'match_videoid_3': videoid_2, 'similarity_score_3': similarity_score_2}

            print("##" * 20)
            ic(newFaceRow)
            print("##" * 20)
            newFaceDF = pd.DataFrame(newFaceRow, index=[0])
            face_match_dataframe = pd.concat([face_match_dataframe, newFaceDF], ignore_index=True)

            # Save the DataFrame as a CSV file
            face_match_dataframe.to_csv(FACE_MATCH_RESULT_CSV_PATH, index=False)
        else:
            print("FACE COMPARISION DATA ALREADY PRESENT IN DATAFRAME.")





if __name__ == "__main__":

    process(transcribe_dataframe, face_match_dataframe)