import numpy as np

from config import *


# current video file name format is 6333460138112_jatin_panwar.mp4
def get_details_from_video_file_name(file_name):
    file_name_separate_list = file_name.split('_')
    file_video_id = file_name_separate_list[0]
    file_name_suffix = file_name_separate_list[1]

    return file_video_id, file_name_suffix

def is_value_present_in_dataframe(file_video_id, dataframe):
    if np.int64(file_video_id) in dataframe['video_id'].values:
        return True
    else:
        return False
