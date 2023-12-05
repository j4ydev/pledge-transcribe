import glob
import os
import shutil

import pandas as pd
from deepface import DeepFace
from icecream import ic

from config import (FACE_IMAGE_DIRECTORY, FACE_IMAGE_FILE_FORMAT,
                    FACE_MATCH_RESULT_CSV_PATH,
                    FACE_MATCH_SAVE_IMAGES_DIRECTORY)
from config import NUMBER_OF_BEST_MATCH_TO_CONSIDER
from utils import get_metadata_from_file_name, is_value_present_in_dataframe

class MATCHFACE():
    def __init__(self):
        self.column_heading_list = ['video_id', 'match_found']
        self.NUMBER_OF_BEST_MATCH_TO_CONSIDER = NUMBER_OF_BEST_MATCH_TO_CONSIDER
        for i in range(0, self.NUMBER_OF_BEST_MATCH_TO_CONSIDER):
            self.column_heading_list.append(f"face_match_{i+1}")
            self.column_heading_list.append(f"distance_indicator_{i+1}")
        if os.path.isfile(FACE_MATCH_RESULT_CSV_PATH):
            try:
                self.face_match_dataframe = pd.read_csv(FACE_MATCH_RESULT_CSV_PATH)
            except Exception as e:
                print(f"{FACE_MATCH_RESULT_CSV_PATH} already present.")
                self.face_match_dataframe = pd.DataFrame(columns=self.column_heading_list)
        else:
            self.face_match_dataframe = pd.DataFrame(columns=self.column_heading_list)


    def process(self, face_images_list):

        for face_image_path in face_images_list:
            ic(face_image_path)
            match_face_image_file_name = face_image_path.split("/")[-1].replace(".png", "")
            file_bid, video_id, file_name_suffix = get_metadata_from_file_name(match_face_image_file_name)
            is_value_present_flag = is_value_present_in_dataframe(video_id, self.face_match_dataframe)

            if not is_value_present_flag:

                dfs = DeepFace.find(img_path = face_image_path, db_path = FACE_IMAGE_DIRECTORY, distance_metric="cosine", model_name="Facenet512")
                print("NUMBER_OF_BEST_MATCH_TO_CONSIDER: ", self.NUMBER_OF_BEST_MATCH_TO_CONSIDER)
                print(type(self.NUMBER_OF_BEST_MATCH_TO_CONSIDER))
                match_face_paths = list(dfs[0].head(self.NUMBER_OF_BEST_MATCH_TO_CONSIDER)["identity"])
                match_face_distance = list(dfs[0].head(self.NUMBER_OF_BEST_MATCH_TO_CONSIDER)["Facenet512_cosine"])
                ic(match_face_distance)

                temp_NUMBER_OF_BEST_MATCH_TO_CONSIDER = self.NUMBER_OF_BEST_MATCH_TO_CONSIDER
                if len(match_face_paths) < self.NUMBER_OF_BEST_MATCH_TO_CONSIDER:
                    temp_NUMBER_OF_BEST_MATCH_TO_CONSIDER = len(match_face_distance)
                match_found = "False"
                new_face_match_row = {'video_id': video_id, 'match_found': match_found}

                for j in range(0,temp_NUMBER_OF_BEST_MATCH_TO_CONSIDER):
                    if len(match_face_distance) >= 2:
                        if match_face_distance[1] < 0.30:
                            match_found = "True"
                            new_face_match_row[f"match_found"] = match_found
                        
                    _, face_video_id, _ = get_metadata_from_file_name(match_face_paths[j].split("/")[-1])
                    new_face_match_row[f"face_match_{j+1}"] = face_video_id
                    new_face_match_row[f"distance_indicator_{j+1}"] = match_face_distance[j]
                    # new_face_match_row = {'video_id': video_id, 'match_found': match_found, 'face_match_1': face_match_person_1_video_id, 'distance_indicator_1': match_face_distance[0], 'face_match_2': face_match_person_2_video_id, 'distance_indicator_2': match_face_distance[1]}

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

                    match_file_bid, match_video_id, match_file_name_suffix = get_metadata_from_file_name(match_face_paths[i])
                    similar_face_image_path = f"{individual_face_match_directory}/{i+1}_{'{:04d}'.format(int(match_face_distance[i]*1000))}_{match_video_id}_{match_file_name_suffix}.png"
                    ic(similar_face_image_path)
                    ic(match_face_paths[i])
                    print("--" * 40)
                    shutil.copy(match_face_paths[i], similar_face_image_path)




if __name__ == "__main__":
    face_images_list = glob.glob(f"{FACE_IMAGE_DIRECTORY}/*")
    face_images_list.sort()

    facematch_obj = MATCHFACE()
    facematch_obj.process(face_images_list)
