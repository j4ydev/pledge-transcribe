import glob

import cv2
import pandas as pd
from deepface import DeepFace
from icecream import ic


# TODO: extract config directories, clean, refactor

class FACEEMBEDDINGS():
    def __init__(self):
        self.ref_image_path = "ref_image.png"
    


    def find_face_embedding(self, new_image_path):
        try:
            result, result_2 = DeepFace.verify(img1_path = self.ref_image_path, img2_path = new_image_path)
            ic(result_2)
        except:
            result_2 = "face not detected"
            print("face not detected")

        return result_2



# if __name__ == "__main__":
#     multi_image_list = glob.glob("face_images/*")
#     print(multi_image_list)
#     single_image_list = glob.glob("face_images_single/*")

#     single_image_list.sort()
#     print("--" * 20)
#     print(single_image_list)
#     compareface_obj = ()
#     compareface_obj.process(single_image_list, multi_image_list)
