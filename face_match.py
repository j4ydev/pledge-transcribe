import glob
import os
import shutil

import pandas as pd
from deepface import DeepFace
from icecream import ic

from config import (FACE_IMAGE_DIRECTORY, FACE_IMAGE_FILE_FORMAT,
                    FACE_MATCH_RESULT_CSV_PATH,
                    FACE_MATCH_SAVE_IMAGES_DIRECTORY)
from utils import get_metadata_from_file_name, is_value_present_in_dataframe


class MATCHFACE():
    def __init__(self):
        if os.path.isfile(FACE_MATCH_RESULT_CSV_PATH):
            try:
                self.face_match_dataframe = pd.read_csv(FACE_MATCH_RESULT_CSV_PATH)
            except:
                self.face_match_dataframe = pd.DataFrame(columns=['video_id', 'match_found', 'face_match_1', 'distance_indicator_1', 'face_match_2', 'distance_indicator_2'])
        else:
            self.face_match_dataframe = pd.DataFrame(columns=['video_id', 'match_found', 'face_match_1', 'distance_indicator_1', 'face_match_2', 'distance_indicator_2'])


    def process(self, face_images_list):

        for face_image_path in face_images_list:

            match_face_image_file_name = face_image_path.split("/")[-1].replace(".png", "")
            file_bid, video_id, file_name_suffix = get_metadata_from_file_name(match_face_image_file_name)
            is_value_present_flag = is_value_present_in_dataframe(video_id, self.face_match_dataframe)


            if not is_value_present_flag:

                dfs = DeepFace.find(img_path = face_image_path, db_path = FACE_IMAGE_DIRECTORY)

                match_face_paths = list(dfs[0].head(5)["identity"])
                match_face_distance = list(dfs[0].head(5)["VGG-Face_cosine"])
                print(type(match_face_distance))
                ic(match_face_distance)



                if len(match_face_paths) >= 2:
                    match_found = "True"
                else:
                    match_found = "False"

                _, face_match_person_1_video_id, _ = get_metadata_from_file_name(match_face_paths[0].split("/")[-1])
                _, face_match_person_2_video_id, _ = get_metadata_from_file_name(match_face_paths[1].split("/")[-1])
                new_face_match_row = {'video_id': video_id, 'match_found': match_found, 'face_match_1': face_match_person_1_video_id, 'distance_indicator_1': match_face_distance[0], 'face_match_2': face_match_person_2_video_id, 'distance_indicator_2': match_face_distance[1]}

                print("##" * 20)
                ic(new_face_match_row)
                print("##" * 20)

                new_face_match_dataframe = pd.DataFrame(new_face_match_row, index=[0])
                self.face_match_dataframe = pd.concat([self.face_match_dataframe, new_face_match_dataframe], ignore_index=True)
                self.face_match_dataframe.to_csv(FACE_MATCH_RESULT_CSV_PATH, index=False)

                ic(video_id)
                for i in range (0, len(match_face_paths)):
                    individual_face_match_directory = f"{FACE_MATCH_SAVE_IMAGES_DIRECTORY}/{video_id}"
                    if not os.path.isdir(individual_face_match_directory):
                        os.mkdir(individual_face_match_directory)

                    similar_face_image_path = f"{individual_face_match_directory}/{i+1}_{'{:04d}'.format(int(match_face_distance[i]*1000))}_{match_face_image_file_name}.png"
                    ic(similar_face_image_path)
                    ic(match_face_paths[i])
                    print("--" * 40)
                    shutil.copy(match_face_paths[i], similar_face_image_path)




if __name__ == "__main__":
    face_images_list = glob.glob(f"{FACE_IMAGE_DIRECTORY}/*{FACE_IMAGE_FILE_FORMAT}")
    face_images_list.sort()

    facematch_obj = MATCHFACE()
    facematch_obj.process(face_images_list)
