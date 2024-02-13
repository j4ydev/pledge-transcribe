import glob
import pandas as pd
from config import (INSPECT_DATAFRAME_PATH, FACE_CAPTURE_CSV_PATH, FACE_IMAGE_DIRECTORY, 
                    FACE_IMAGE_FILE_FORMAT, MANUAL_FACE_CAPTURE_DIRECTORY, FINAL_FACES_DIRECTORY, 
                    FINAL_FACES_CSV_PATH, MANUAL_FACE_IMAGE_FILE_FORMAT, FLATTEN_CSV_FILE_PATH, FLATTEN_IMAGE_DIRECTORY)
from utils import get_metadata_from_file_name, is_value_present_in_dataframe
import os
import shutil
from deepface import DeepFace


class GATHERFACES():
    def __init__(self):
        self.capture_face_dataframe = pd.read_csv(FACE_CAPTURE_CSV_PATH)
        self.inspect_dataframe = pd.read_csv(INSPECT_DATAFRAME_PATH)
        self.auto_captured_image_list = glob.glob(f"{FACE_IMAGE_DIRECTORY}/*{FACE_IMAGE_FILE_FORMAT}")
        # self.ledger_dataframe = pd.read_csv(LEDGER_CSV_PATH)
        self.flatten_dataframe = pd.read_csv(FLATTEN_CSV_FILE_PATH)

        if os.path.isfile(FINAL_FACES_CSV_PATH):
            try:
                self.final_face_dataframe = pd.read_csv(FINAL_FACES_CSV_PATH)
            except Exception as e:
                print(f"{FINAL_FACES_CSV_PATH} already present.")
                self.final_face_dataframe = pd.DataFrame(columns=['video_id', 'auto_face_found', 'file_gathered', 'face_found'])
        else:
            self.final_face_dataframe = pd.DataFrame(columns=['video_id', 'auto_face_found', 'file_gathered', 'face_found'])


        if not os.path.isdir(FINAL_FACES_DIRECTORY):
            os.makedirs(FINAL_FACES_DIRECTORY)

    def remove_unnecessary_columns(self):
        df = self.inspect_dataframe
        df2 = df[['vid','batch Number', 'InvigilationState']]
        df2 = df2.rename(columns={'vid': 'video_id', 'batch Number':'batch_number', 'InvigilationState': 'approval'})
        return df2

    def verify_video_id(self, approval_dataframe, video_id):
        try:
            approval_status = approval_dataframe.loc[approval_dataframe['video_id'] == video_id, 'approval'].iloc[0]
            return True
        except:
            print(f"{video_id} not present in approval_dataframe.")
            return False
        
    def verify_face(self, img1_path, img2_path):
        try:
            result = DeepFace.verify(img1_path , img2_path)
            found_face_flag = True
        except Exception as e:
            found_face_flag = False
        return found_face_flag

    # def get_manual_face_capture_images_list(self, batch_number):
    #     manually_captured_image_list = glob.glob(f"{MANUAL_FACE_CAPTURE_DIRECTORY}/{batch_number}/*{MANUAL_FACE_IMAGE_FILE_FORMAT}")
    #     return manually_captured_image_list

    def get_image_from_auto_face_capture_directory(self, video_id):
        for image_path in self.auto_captured_image_list:
            image_name = image_path.split("/")[-1].replace(f"{FACE_IMAGE_FILE_FORMAT}", "")
            file_bid, video_id_, file_name_suffix = get_metadata_from_file_name(image_name)
            
            if str(video_id) == str(video_id_):
                print("-- copying image. --")
                shutil.copy(image_path , f"{FINAL_FACES_DIRECTORY}/")
                new_final_face_raw = {'video_id': video_id,  'auto_face_found': True, 'file_gathered': True, "face_found": True}
                new_final_face_dataframe = pd.DataFrame(new_final_face_raw, index=[0])

                self.final_face_dataframe = pd.concat([self.final_face_dataframe, new_final_face_dataframe], ignore_index=True)
                self.final_face_dataframe.to_csv(FINAL_FACES_CSV_PATH, index=False)

    def get_image_from_manual_face_capture_directory(self, video_id, batch_number):
        video_id_found_status = False
        # manually_captured_image_list = self.get_manual_face_capture_images_list(batch_number)

        # for image_path in manually_captured_image_list:
        #     
        #     file_bid, video_id_, file_name_suffix = get_metadata_from_file_name(image_name)

        if video_id in self.flatten_dataframe["video_id"].values:
            manual_image_path = self.flatten_dataframe.loc[self.flatten_dataframe['video_id'] == video_id, 'manual_image_file_path'].iloc[0]
            if self.verify_face(manual_image_path,manual_image_path):
                print(f" {video_id} -------------- copying image. --")
                image_name = manual_image_path.split("/")[-1].replace(f"{FACE_IMAGE_FILE_FORMAT}", "")
                shutil.copy(manual_image_path , f"{FINAL_FACES_DIRECTORY}/{image_name}{FACE_IMAGE_FILE_FORMAT}")
                video_id_found_status = True

                new_final_face_raw = {'video_id': video_id, 'auto_face_found': False, 'file_gathered': True, "face_found": True}
                new_final_face_dataframe = pd.DataFrame(new_final_face_raw, index=[0])

                self.final_face_dataframe = pd.concat([self.final_face_dataframe, new_final_face_dataframe], ignore_index=True)
                self.final_face_dataframe.to_csv(FINAL_FACES_CSV_PATH, index=False)
            else:
                print(f"{video_id} ------- face not found in manually uploaded image. ---")
                video_id_found_status = True
                new_final_face_raw = {'video_id': video_id, 'auto_face_found': False, 'file_gathered': True, "face_found": False}
                new_final_face_dataframe = pd.DataFrame(new_final_face_raw, index=[0])

                self.final_face_dataframe = pd.concat([self.final_face_dataframe, new_final_face_dataframe], ignore_index=True)
                self.final_face_dataframe.to_csv(FINAL_FACES_CSV_PATH, index=False)
        
        else:
            new_final_face_raw = {'video_id': video_id, 'auto_face_found': False, 'file_gathered': False, "face_found": False}
            new_final_face_dataframe = pd.DataFrame(new_final_face_raw, index=[0])
            print(f"{video_id} videoid not found in manually uploaded face images.")
            self.final_face_dataframe = pd.concat([self.final_face_dataframe, new_final_face_dataframe], ignore_index=True)
            self.final_face_dataframe.to_csv(FINAL_FACES_CSV_PATH, index=False)

    def process(self):
        
        approval_dataframe = self.remove_unnecessary_columns()
        
        print(approval_dataframe.head())
        for index, row in approval_dataframe.iterrows():
            video_id = row['video_id']
            is_value_present_flag = is_value_present_in_dataframe(video_id, self.final_face_dataframe)

            if not is_value_present_flag:
                approval_status = approval_dataframe.loc[approval_dataframe['video_id'] == video_id, 'approval'].iloc[0]
                batch_number = approval_dataframe.loc[approval_dataframe['video_id'] == video_id, 'batch_number'].iloc[0]

                if video_id in self.capture_face_dataframe["video_id"].values:
                    auto_face_found_status = self.capture_face_dataframe.loc[self.capture_face_dataframe['video_id'] == video_id, 'face_found'].iloc[0]
                else:
                    if approval_status == "Accept":
                        self.get_image_from_manual_face_capture_directory(video_id, batch_number)
                        continue


                #CASE:1
                if approval_status == "Accept" and auto_face_found_status == True:
                    self.get_image_from_auto_face_capture_directory(video_id)
                #CASE:2
                elif approval_status == "Accept" and auto_face_found_status == False:
                    self.get_image_from_manual_face_capture_directory(video_id, batch_number)

if __name__ == "__main__":
    gather_faces_obj = GATHERFACES()
    manually_captured_image_list = glob.glob(f"{FLATTEN_IMAGE_DIRECTORY}/*{MANUAL_FACE_IMAGE_FILE_FORMAT}")
    gather_faces_obj.process()