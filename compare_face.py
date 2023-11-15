from deepface import DeepFace
import glob
from icecream import ic
import cv2

import pandas as pd

class COMPAREFACE():
    def __init__(self):
        # self.df = pd.DataFrame(columns=['videoFilePath','similar_face_name_score','maximin_score', 'maximum_score_face_name'])
        self.df =  pd.DataFrame(columns=['image_name', 'embedding'])

    def main(self, images_list, ref_image, single_image_path):
        minimum_score = 1
        minimum_score_image = ""
        minimum_score_result = None
        similar_face_score_dict = {}

        for image_path in images_list:
            face_image = cv2.imread(image_path)
            try:
                result, result_2 = DeepFace.verify(img1_path = ref_image, img2_path = face_image)
                ic(result)
                ic(result_2)
                # a =input()

                new_row = {
                    'image_name':image_path.split("/")[-1],
                    'embedding': result_2,
                }

                # new_df = pd.DataFrame(new_row, index=[0])
                # self.df = pd.concat([self.df, new_df], ignore_index=True)
                #     # similar_face_score_dict[str(result["distance"])] = str(image_path)

                #     # if float(result["distance"]) < minimum_score:
                #     #     minimum_score = float(result["distance"])
                #     #     minimum_score_image = image_path
                #     #     minimum_score_result = result
                # self.df.to_csv("face_compare_score.csv", index=False)

            except:
                result_2 = "face not detected" 
                print("face not detected")

            new_row = {
                    'image_name':image_path.split("/")[-1],
                    'embedding': result_2,
                }

            new_df = pd.DataFrame(new_row, index=[0])
            self.df = pd.concat([self.df, new_df], ignore_index=True)
            self.df.to_csv("face_compare_score.csv", index=False)

            
        # ic(minimum_score)
        # ic(minimum_score_image)
        # ic(minimum_score_result)
        
        # sorted_dict = dict(sorted(similar_face_score_dict.items()))

        # if len(sorted_dict) > 5:
        #     first_five_pairs = list(sorted_dict.items())[:5]
        # else:
        #     first_five_pairs = list(sorted_dict.items())[:len(sorted_dict)]

        # return minimum_score, minimum_score_image, first_five_pairs

    def process(self, single_image_list, multi_image_list):
        for single_image_path in single_image_list:
            single_image = cv2.imread(single_image_path)
            minimum_score, minimum_score_image, first_five_pairs = self.main(multi_image_list, single_image, single_image_path)
            a = input()
            # Save the DataFrame as a CSV file


    





if __name__ == "__main__":
    multi_image_list = glob.glob("face_images/*")
    print(multi_image_list)
    single_image_list = glob.glob("face_images_single/*")
    
    single_image_list.sort()
    print("--" * 20)
    print(single_image_list)
    compareface_obj = COMPAREFACE()
    compareface_obj.process(single_image_list, multi_image_list)
