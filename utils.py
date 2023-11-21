### GET DETAILS FROM VIDEO FILE NAME ###
import numpy as np
from config import *


def get_details_from_video_name(file_name):

    file_name_separate_list = file_name.split("_")
    file_videoid = file_name_separate_list[0]
    file_name_suffix = file_name_separate_list[1]

    return file_videoid, file_name_suffix

def is_value_present_in_dataframe(file_video_id, dataframe):

    if np.int64(file_video_id) in dataframe["vid"].values:
        return True
    else:
        return False
