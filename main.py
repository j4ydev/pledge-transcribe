from video_transcribe import TRANSCRIBE
from capture_face_img import GETFRAME
from face_embedding import FACEEMBEDDINGS
import glob
import pandas as pd
import time
import os
from icecream import ic
import cv2

transcribe_obj = TRANSCRIBE()
getframe_obj = GETFRAME()
faceembeddings_obj = FACEEMBEDDINGS()

### ALL PATHS WILL BE DEFINED HERE ###
# TODO: move "separated/mdx_extra" -> "output/separated/mdx_extra"
BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY = "separated/mdx_extra"
TRANSCRIBED_FILE_PATH = "output/transcribe_text.csv" ### PATH OF THE OUTPUT CSV FILE
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


def process(transcribe_dataframe):
    dir = INPUT_VIDEO_DIRECTORY
    inputVideoFilesList = glob.glob(f"{dir}/*.mp4")
    inputVideoFilesList.sort()
    print(inputVideoFilesList)

    for videoFilePath in inputVideoFilesList:
        print(videoFilePath)


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
            
            frame = getframe_obj.getImageFromVideo(videoFilePath)
            frame_filepath = f'{IMAGE_SAVE_DIRECTORY}/{imageFileName}'
            # Save the frame as an image
            print(frame_filepath)
            print("--")
            cv2.imwrite(frame_filepath, frame)


            # MODULE:3 ------> SAVE IMAGE EMBEDDINGS 
            embeddings_data = faceembeddings_obj.find_face_embedding(frame_filepath)

            ### create image_index file
            imageIndexFileName = videoFilePath.split("/")[-1].replace(".mp4", ".txt")
            imageIndexFilePath = f"{IMAGE_INDEX_DIRECTORY}/{imageIndexFileName}"

            with open(imageIndexFilePath, 'w') as f:
                f.write(str(embeddings_data))

        




if __name__ == "__main__":

    process(transcribe_dataframe)