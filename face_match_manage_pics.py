import pandas as pd
from config import (FIND_FACES_API_CSV, FINAL_FACES_DIRECTORY, FACE_IMAGE_FILE_FORMAT, 
                    SIMILAR_PLEDGE_TAKERS_API_DIRECTORY, FIND_FACES_MANAGE_PICS_ERROR_CSV)
import glob
from utils import get_metadata_from_file_name
import os
import shutil
from icecream import ic

class MANAGEFACEMATCHPICS():
    def __init__(self):
        # self.accepted_video_faces_list = glob.glob(f"{FINAL_FACES_DIRECTORY}/*{FACE_IMAGE_FILE_FORMAT}")
        self.accepted_video_faces_list = glob.glob("output/accepted_video_faces_1/*.png")
        ic(self.accepted_video_faces_list)
        if not os.path.isdir(SIMILAR_PLEDGE_TAKERS_API_DIRECTORY):
            os.mkdir(SIMILAR_PLEDGE_TAKERS_API_DIRECTORY)

        if os.path.isfile(FIND_FACES_MANAGE_PICS_ERROR_CSV):
            try:
                self.find_faces_manage_pics_error_dataframe = pd.read_csv(FIND_FACES_MANAGE_PICS_ERROR_CSV)
            except Exception as e:
                print(f"{FIND_FACES_MANAGE_PICS_ERROR_CSV} already present.")
                self.find_faces_manage_pics_error_dataframe = pd.DataFrame(columns=['video_id'])
        else:
            self.find_faces_manage_pics_error_dataframe = pd.DataFrame(columns=['video_id'])


    def find_face_image_path(self, video_id):
        ic(video_id)
        for image_path in self.accepted_video_faces_list:
            image_name = image_path.split("/")[-1].replace(FACE_IMAGE_FILE_FORMAT, "")
            _,video_id_, file_name_suffix = get_metadata_from_file_name(image_name)
            if str(video_id) == str(video_id_):
                return image_path, video_id_,  file_name_suffix


    def identity_number_of_face_matches(self, row_data):
        length = len(row_data)
        length = length - 4

        number_of_faces = length//2
        return number_of_faces

    def process(self, face_recognition_dataframe):
        for index, row in face_recognition_dataframe.iterrows():
            row = {key: value for key, value in row.items() if not pd.isna(value)}
            source_video_id = row["video_id"]
            # print("--------------------------------")
            try:
                source_image_path, video_id, file_name_suffix = self.find_face_image_path(source_video_id)

                if not os.path.isdir(f"{SIMILAR_PLEDGE_TAKERS_API_DIRECTORY}/{source_video_id}"):
                    os.mkdir(f"{SIMILAR_PLEDGE_TAKERS_API_DIRECTORY}/{source_video_id}")
                    copy_target_path = f"{SIMILAR_PLEDGE_TAKERS_API_DIRECTORY}/{source_video_id}/0_{video_id}_{file_name_suffix}{FACE_IMAGE_FILE_FORMAT}"
                    if not os.path.isfile(copy_target_path):
                        shutil.copy(source_image_path, copy_target_path)
                
                num_of_faces = self.identity_number_of_face_matches(row)
                # ic(num_of_faces)
                # print("--- --- " * 20 )
                for i in range(1, num_of_faces):
                    video_id_of_matched_user = int(row[f"face_match_{i}"])
                    # ic(video_id_of_matched_user)
                    image_path, target_video_id,  file_name_suffix = self.find_face_image_path(video_id_of_matched_user)
                    copy_target_path = f"{SIMILAR_PLEDGE_TAKERS_API_DIRECTORY}/{source_video_id}/{i}_{target_video_id}_{file_name_suffix}{FACE_IMAGE_FILE_FORMAT}"
                    # ic(image_path)
                    # ic(copy_target_path)
                    if not os.path.isfile(copy_target_path):
                        shutil.copy(source_image_path, copy_target_path)
            except:
                new_find_faces_manage_pics_error_raw = {'video_id': str(source_video_id)}
                new_find_face_manage_pics_error_dataframe = pd.DataFrame(new_find_faces_manage_pics_error_raw, index=[0])
                self.find_faces_manage_pics_error_dataframe = pd.concat([self.find_faces_manage_pics_error_dataframe, new_find_face_manage_pics_error_dataframe], ignore_index=True)
                self.find_faces_manage_pics_error_dataframe.to_csv(FIND_FACES_MANAGE_PICS_ERROR_CSV, index=False)


if __name__ == '__main__':
    manage_face_match_pics_obj = MANAGEFACEMATCHPICS()
    face_recognition_dataframe = pd.read_csv(FIND_FACES_API_CSV)
    manage_face_match_pics_obj.process(face_recognition_dataframe)