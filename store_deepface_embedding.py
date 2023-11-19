import glob
import os

from deepface import DeepFace

from config import *


# TODO: extract config directories, clean, refactor
class FACEEMBEDDINGS():
    def __init__(self):
        self.ref_image_path = "ref_image.png"

    def find_face_embedding(self, new_image_path):
        try:
            result, result_2 = DeepFace.verify(img1_path = self.ref_image_path, img2_path = new_image_path)
        except:
            result_2 = "face not detected"
            print("face not detected")
        return result_2

    def check_if_embedding_present(self, image_file_name):
        possible_screenshot_path = f"{FACE_IMAGE_INDEX_DIRECTORY}/{image_file_name}"
        if os.path.isfile(possible_screenshot_path):
            return True
        else:
            return False

    def process(self, face_image_files_list):
        for face_images_path in face_image_files_list:
            image_index_file_name = face_images_path.split("/")[-1].replace(".png", ".txt")
            image_index_file_path = f"{FACE_IMAGE_INDEX_DIRECTORY}/{image_index_file_name}"
            embedding_present_flag = self.check_if_embedding_present(image_index_file_path)
            if embedding_present_flag == False:
                result, result_2_embedding_data = DeepFace.verify(img1_path = self.ref_image_path, img2_path = face_images_path)
            else:
                print("EMBEDDING ALREADY PRESENT IN DIRECTORY.")
            with open(image_index_file_path, 'w') as f:
                f.write(str(result_2_embedding_data))
        return "Complete"


if __name__ == "__main__":
    faceembedding_obj = FACEEMBEDDINGS()
    faceImageFilesList = glob.glob(f"{FACE_IMAGE_DIRECTORY}/*.png")
    faceImageFilesList.sort()
    faceembedding_obj.process(faceImageFilesList)