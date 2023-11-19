import glob
import os

import cv2
import numpy as np
import pandas as pd
from deepface import DeepFace
from icecream import ic

from config import *
from utils import *

# TODO: extract config directories, clean, refactor

class COMPAREFACE():
    def __init__(self):
        ### IF FACEMATCHING DATAFRAME EXIST OR NOT EXISTS ###
        if os.path.isfile(FACE_MATCH_RESULT_CSV_PATH):
            try:
                self.face_match_dataframe = pd.read_csv(FACE_MATCH_RESULT_CSV_PATH)
            except:
                self.face_match_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'video-id_1', 'similarity_score_1','video-id_2','similarity_score_2', 'video-id_3','similarity_score_3'])
        else:
            self.face_match_dataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'vid', 'match_videoid_1', 'similarity_score_1','match_videoid_2','similarity_score_2', 'match_videoid_3','similarity_score_3'])

    ### GET DETAILS FROM VIDEO FILE NAME ###
    def get_details_from_video_name(self, file_name):
        file_name_separate_list = file_name.split("_")
        file_row = file_name_separate_list[1]
        file_column = file_name_separate_list[2]
        file_index = 4*(int(file_row)-1) + int(file_column)
        file_pagenumber = file_name_separate_list[0]
        file_video_id = file_name_separate_list[3]

        return file_row, file_column, file_index, file_pagenumber, file_video_id

    ### GET 2 CLOSEST FACES AND THEIR SCORE FROM DIRECTORY. ###
    def find_videoid_and_score(self, first_two_pairs):
        first_two_pairs = dict(first_two_pairs)
        first_distance = True
        for distance in first_two_pairs:
            file_row, file_column, file_index, file_pagenumber, file_video_id = get_details_from_video_name(first_two_pairs[distance].split("/")[-1].replace(".mp4",""))
            if first_distance:
                first_distance = False
                videoid_1 = file_video_id
                similarity_score_1 = 1 - float(distance)
                ic(videoid_1)
            else:
                videoid_2 = file_video_id
                similarity_score_2 = 1 - float(distance)
        return videoid_1, similarity_score_1, videoid_2, similarity_score_2

    def process(self, face_embedding_list):
        for face_embedding_path in face_embedding_list:
            # MODULE:4 ------> COMPARE IMAGE WITH OTHER IMAGES
            embeddingFileName = face_embedding_path.split("/")[-1].replace(".txt","")
            file_row, file_column, file_index, file_pagenumber, file_video_id = self.get_details_from_video_name(embeddingFileName)
            is_face_embedding_present_flag = is_value_present_in_dataframe(file_index, self.face_match_dataframe)
            similar_face_score_dict = {}
            if not is_face_embedding_present_flag:
                with open(face_embedding_path, "r") as f:
                    current_image_embedding = f.read()
                current_image_embedding = eval(current_image_embedding)
                for embedding_path in face_embedding_list:
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
                videoid_1, similarity_score_1, videoid_2, similarity_score_2 = self.find_videoid_and_score(first_two_pairs)
                # INSERT DATA IN DATAFRAME
                new_face_row = {'row': file_row, 'column': file_column, 'index': file_index, 'pagenumber': file_pagenumber, 'vid': file_video_id, 'match_videoid_1': file_video_id, 'similarity_score_1': 1,'match_videoid_2': videoid_1, 'similarity_score_2': similarity_score_1, 'match_videoid_3': videoid_2, 'similarity_score_3': similarity_score_2}
                new_face_dataframe = pd.DataFrame(new_face_row, index=[0])
                self.face_match_dataframe = pd.concat([self.face_match_dataframe, new_face_dataframe], ignore_index=True)
                # Save the DataFrame as a CSV file
                self.face_match_dataframe.to_csv(FACE_MATCH_RESULT_CSV_PATH, index=False)
            else:
                print("FACE COMPARISION DATA ALREADY PRESENT IN DATAFRAME.")

if __name__ == "__main__":
    compareface_obj = COMPAREFACE()
    face_embedding_list = glob.glob(f"{FACE_IMAGE_INDEX_DIRECTORY}/*.txt")
    face_embedding_list.sort()
    compareface_obj.process(face_embedding_list)
