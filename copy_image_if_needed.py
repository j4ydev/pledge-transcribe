import pandas as pd
import glob
from utils import get_metadata_from_file_name
import shutil
from config import FACE_CAPTURE_CSV_PATH, FACE_IMAGE_DIRECTORY, FACE_IMAGE_FILE_FORMAT, MANUAL_FACE_CAPTURE_DIRECTORY

capture_face_dataframe = pd.read_csv(FACE_CAPTURE_CSV_PATH)
invigilation_images_list = glob.glob(f"{MANUAL_FACE_CAPTURE_DIRECTORY}/*.{FACE_IMAGE_FILE_FORMAT}") # capture images manually directory path 

for index, row in capture_face_dataframe.iterrows():
    video_id = row['video_id']
    face_found_status = capture_face_dataframe.loc[capture_face_dataframe['video_id'] == video_id, 'face_found'].iloc[0]
    approval_status = capture_face_dataframe.loc[capture_face_dataframe['video_id'] == video_id, 'inspect_csv_status'].iloc[0]

    
    if str(face_found_status) == "False" and approval_status == "Accept":
            copy_status = False
            for image_path in invigilation_images_list:
                image_name = image_path.split("/")[-1].replace(f".{FACE_IMAGE_FILE_FORMAT}", "")
                file_bid, video_id_, file_name_suffix = get_metadata_from_file_name(image_name)
                
                if str(video_id) == str(video_id_):
                    print("-- copying image. --")
                    shutil.copy(image_path , f"{FACE_IMAGE_DIRECTORY}/")
                    copy_status = True
            if not copy_status:
                print("user not found in manually uploaded face images.")
                    

