from video_transcribe import TRANSCRIBE
from capture_face_img import GETFRAME
from face_embedding import FACEEMBEDDINGS
import glob
import pandas as pd
import time
import os
from icecream import ic
import cv2
from deepface.commons import functions, realtime, distance as dst
import numpy as np

transcribe_obj = TRANSCRIBE()
getframe_obj = GETFRAME()
faceembeddings_obj = FACEEMBEDDINGS()

### ALL PATHS WILL BE DEFINED HERE ###
# TODO: move "separated/mdx_extra" -> "output/separated/mdx_extra"
BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY = "separated/mdx_extra"
TRANSCRIBED_FILE_PATH = "output/transcribe_text.csv" ### PATH OF THE OUTPUT CSV FILE
FACE_MATHCING_CSV_PATH = "output/face_match.csv"
INPUT_VIDEO_DIRECTORY = "/Users/jay/work/new_video" ### DIRECTORY OF VIDEO FILES (DO NOT ADD / AT THE END OF THE PATH)
IMAGE_SAVE_DIRECTORY = "output/screenshots" # PATH DIR OF SAVE FRAME FROM VIDEO (DO NOT ADD / AT THE END OF PATH)
IMAGE_INDEX_DIRECTORY = "output/image_index"




### IF DATAFRAME EXIST OR NOT EXISTS ###
if os.path.isfile(TRANSCRIBED_FILE_PATH):
    try:
        transcribe_dataframe = pd.read_csv(TRANSCRIBED_FILE_PATH)
    except:
        transcribe_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'videoid', 'timeconsumed', 'transcribetext'])
else:
    transcribe_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'videoid', 'timeconsumed', 'transcribetext'])

if os.path.isfile(FACE_MATHCING_CSV_PATH):
    try:
        face_match_dataframe = pd.read_csv(FACE_MATHCING_CSV_PATH)
    except:
        face_match_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pageNumber', 'video-id_1', 'similarity_score_1','video-id_2','similarity_score_2', 'video-id_3','similarity_score_3'])
else:
    face_match_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pageNumber', 'videoid', 'match_videoid_1', 'similarity_score_1','match_videoid_2','similarity_score_2', 'match_videoid_3','similarity_score_3'])

def get_details_from_video_name(file_name):
    file_name_separate_list = file_name.split("_")
    file_row = file_name_separate_list[1]
    file_column = file_name_separate_list[2]
    file_index = 4*(int(file_row)-1) + int(file_column)
    file_pagenumber = file_name_separate_list[0]
    file_videoid = file_name_separate_list[3]

    return file_row, file_column, file_index, file_pagenumber, file_videoid
    
### CHECK IF VIDEO IS ALREADY PROCESSED OR NOT ###
def is_value_present(index_number, dataframe):
    if index_number in dataframe["index"].values:
        return True
    else:
        return False

def check_if_screenshot_present(imageFileName):
    possible_screenshot_path = f"{IMAGE_SAVE_DIRECTORY}/{imageFileName}"
    if os.path.isfile(possible_screenshot_path):
        return True
    else:
        return False

def capture_face_image_and_embedding(videoFilePath, imageFileName):
    frame = getframe_obj.getImageFromVideo(videoFilePath)
    frame_filepath = f'{IMAGE_SAVE_DIRECTORY}/{imageFileName}'
    # Save the frame as an image
    print(frame_filepath)
    print("--")
    cv2.imwrite(frame_filepath, frame)

    embeddings_data = faceembeddings_obj.find_face_embedding(frame_filepath)
    # print("embeddings_data", embeddings_data)
    # print("__"* 40)
    # print(type(embeddings_data))
    if embeddings_data == "face not detected" or embeddings_data == "None":
        # print("calling recurrent model")
        # a = input()
        embeddings_data = capture_face_image_and_embedding(videoFilePath, imageFileName)
    else:
        pass
    return embeddings_data

def find_videoid_and_score(first_two_pairs):
    first_two_pairs = dict(first_two_pairs)
    first_distance = True
    for distance in first_two_pairs:
        print("aaaa",first_two_pairs[distance])
        file_row, file_column, file_index, file_pagenumber, file_videoid = get_details_from_video_name(first_two_pairs[distance].split("/")[-1].replace(".mp4",""))
        if first_distance:
            first_distance = False
            videoid_1 = file_videoid
            similarity_score_1 = 1 - float(distance)
            ic(videoid_1)
            print("@@"* 50)
        else:
            videoid_2 = file_videoid
            similarity_score_2 = 1 - float(distance)
    return videoid_1, similarity_score_1, videoid_2, similarity_score_2

def process(transcribe_dataframe, face_match_dataframe):
    inputVideoFilesList = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*.mp4")
    inputVideoFilesList.sort()

    # print(inputVideoFilesList)

    for videoFilePath in inputVideoFilesList:
        ic(videoFilePath)

        embeddingFilesList = glob.glob(f"{IMAGE_INDEX_DIRECTORY}/*.txt")
        embeddingFilesList.sort()

        # GET DETAILS OF VIDEO FROM VIDEO FILE NAME
        file_name = videoFilePath.split("/")[-1].replace(".mp4","")
        file_row, file_column, file_index, file_pagenumber, file_videoid = get_details_from_video_name(file_name)

        is_value_present_flag = is_value_present(file_index, transcribe_dataframe)

        if not is_value_present_flag:
            # MODULE:1 ------> TRANSCRIBE VIDEO PROCESS 
            start_time = time.time()
            file_transcribetext = transcribe_obj.transcribe(videoFilePath)
            end_time = time.time()
            time_consumed = end_time - start_time

            # INSERT DATA IN DATAFRAME 
            new_row = {'row': file_row, 'column': file_column, 'index': file_index, 'pagenumber': file_pagenumber, 'videoid': file_videoid, 'timeconsumed': time_consumed, 'transcribetext': file_transcribetext}
            print("##" * 20)
            ic(new_row)
            print("##" * 20)
            new_df = pd.DataFrame(new_row, index=[0])
            transcribe_dataframe = pd.concat([transcribe_dataframe, new_df], ignore_index=True)

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
            embeddings_data = capture_face_image_and_embedding(videoFilePath, imageFileName)
            ### create image_index file
            imageIndexFileName = videoFilePath.split("/")[-1].replace(".mp4", ".txt")
            imageIndexFilePath = f"{IMAGE_INDEX_DIRECTORY}/{imageIndexFileName}"

            with open(imageIndexFilePath, 'w') as f:
                f.write(str(embeddings_data))

            # MODULE:4 ------> COMPARE IMAGE WITH OTHER IMAGES
            current_image_embedding = embeddings_data
            similar_face_score_dict = {}

            for embedding_path in embeddingFilesList:
                print(embedding_path)
                with open(embedding_path, "r") as f:
                    image_from_dir = f.read()
                print("::" * 20)
                

                if image_from_dir != "face not detected":
                    image_from_dir = eval(image_from_dir)
                    # distance = dst.findCosineDistance(current_image_embedding, image_from_dir)
                    a = np.matmul(np.transpose(np.array(image_from_dir[0]["embedding"])), np.array(current_image_embedding[0]["embedding"]))
                    b = np.sum(np.multiply(np.array(image_from_dir[0]["embedding"]), np.array(image_from_dir[0]["embedding"])))
                    c = np.sum(np.multiply(np.array(current_image_embedding[0]["embedding"]), np.array(current_image_embedding[0]["embedding"])))

                    distance = 1 - (a / (np.sqrt(b) * np.sqrt(c)))

                else:
                    distance = 0
                # ic(distance)
                similar_face_score_dict[str(distance)] = embedding_path
            sorted_dict = dict(sorted(similar_face_score_dict.items()))

            if len(sorted_dict) > 2:
                first_two_pairs = list(sorted_dict.items())[:2]
            else:
                first_two_pairs = list(sorted_dict.items())[:len(sorted_dict)]

            ic(first_two_pairs)
            if len(first_two_pairs) >= 2:
                videoid_1, similarity_score_1, videoid_2, similarity_score_2 = find_videoid_and_score(first_two_pairs)

            else:
                videoid_1, similarity_score_1, videoid_2, similarity_score_2 = 0, None, 0, None
            # INSERT DATA IN DATAFRAME 
            new_row_face = {'row': file_row, 'column': file_column, 'index': file_index, 'pagenumber': file_pagenumber, 'videoid': file_videoid, 'match_videoid_1': file_videoid, 'similarity_score_1': 1,'match_videoid_2': videoid_1, 'similarity_score_2': similarity_score_1, 'match_videoid_3': videoid_2, 'similarity_score_3': similarity_score_2}

            print("##" * 20)
            ic(new_row_face)
            print("##" * 20)
            new_df_face = pd.DataFrame(new_row_face, index=[0])
            face_match_dataframe = pd.concat([face_match_dataframe, new_df_face], ignore_index=True)

            # Save the DataFrame as a CSV file
            face_match_dataframe.to_csv(FACE_MATHCING_CSV_PATH, index=False)
            




if __name__ == "__main__":

    process(transcribe_dataframe, face_match_dataframe)