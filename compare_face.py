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
        if os.path.isfile(FACE_MATCHING_CSV_PATH):
            try:
                self.faceMatchDataframe = pd.read_csv(FACE_MATCHING_CSV_PATH)
            except:
                self.faceMatchDataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'video-id_1', 'similarity_score_1','video-id_2','similarity_score_2', 'video-id_3','similarity_score_3'])
        else:
            self.faceMatchDataframe = pd.DataFrame(columns=['row', 'column', 'index', 'pagenumber', 'videoid', 'match_videoid_1', 'similarity_score_1','match_videoid_2','similarity_score_2', 'match_videoid_3','similarity_score_3'])

    ### GET DETAILS FROM VIDEO FILE NAME ###
    def get_details_from_video_name(self, file_name):
        file_name_separate_list = file_name.split("_")
        file_row = file_name_separate_list[1]
        file_column = file_name_separate_list[2]
        file_index = 4*(int(file_row)-1) + int(file_column)
        file_pagenumber = file_name_separate_list[0]
        file_videoid = file_name_separate_list[3]

        return file_row, file_column, file_index, file_pagenumber, file_videoid

    ### GET 2 CLOSEST FACES AND THEIR SCORE FROM DIRECTORY. ###
    def find_videoid_and_score(self, first_two_pairs):
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

    def process(self, faceEmbeddingList):
        print(faceEmbeddingList)
        for faceEmbeddingPath in faceEmbeddingList:
            # MODULE:4 ------> COMPARE IMAGE WITH OTHER IMAGES
            embeddingFileName = faceEmbeddingPath.split("/")[-1].replace(".txt","")
            file_row, file_column, file_index, file_pagenumber, file_videoid = self.get_details_from_video_name(embeddingFileName)
            is_face_embedding_present_flag = is_value_present_in_dataframe(file_index, self.faceMatchDataframe)
            similar_face_score_dict = {}
            if not is_face_embedding_present_flag:
                with open(faceEmbeddingPath, "r") as f:
                    current_image_embedding = f.read()
                current_image_embedding = eval(current_image_embedding)
                for embedding_path in faceEmbeddingList:
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
                newFaceRow = {'row': file_row, 'column': file_column, 'index': file_index, 'pagenumber': file_pagenumber, 'videoid': file_videoid, 'match_videoid_1': file_videoid, 'similarity_score_1': 1,'match_videoid_2': videoid_1, 'similarity_score_2': similarity_score_1, 'match_videoid_3': videoid_2, 'similarity_score_3': similarity_score_2}
                newFaceDF = pd.DataFrame(newFaceRow, index=[0])
                self.faceMatchDataframe = pd.concat([self.faceMatchDataframe, newFaceDF], ignore_index=True)
                # Save the DataFrame as a CSV file
                self.faceMatchDataframe.to_csv(FACE_MATCHING_CSV_PATH, index=False)
            else:
                print("FACE COMPARISION DATA ALREADY PRESENT IN DATAFRAME.")

if __name__ == "__main__":
    compareface_obj = COMPAREFACE()
    faceEmbeddingList = glob.glob(f"{IMAGE_INDEX_DIRECTORY}/*.txt")
    faceEmbeddingList.sort()
    compareface_obj.process(faceEmbeddingList)
