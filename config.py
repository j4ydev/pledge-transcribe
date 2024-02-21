WORKING_DIR_PREFIX_JAY = "/Users/jay"
WORKING_DIR_PREFIX_SID = "/Users/khasgiwa/Workbench"
WORKING_DIR_PREFIX = WORKING_DIR_PREFIX_SID

BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY = "output/audio_from_video"
BACKGROUND_NOISE_REMOVED_AUDIO_SUB_DIRECTORY = "mdx_extra"
BACKGROUND_REMOVED_FILE_NAME = "vocals.mp3"
AUDIO_FILE_FORMAT = ".mp3"
FAILED_TRANSCRIBE_CSV_PATH = "output/error/failed_transcribe.csv"
FAILED_VIDEO_2_AUDIO_CSV_PATH = "output/error/failed_video2audio.csv"

FACE_MATCH_SAVE_IMAGES_DIRECTORY = "output/similar_pledge_takers"
VGG_FACE_MATCH_SAVE_IMAGES_DIRECTORY = "output/similar_pledge_takers_vggface"
FACENET512_MATCH_SAVE_IMAGES_DIRECTORY = "output/similar_pledge_takers_facenet512"

FACE_CAPTURE_CSV_PATH = "output/capture_face.csv"
FACE_IMAGE_DIRECTORY = "output/screenshots" # PATH DIR OF SAVE FRAME FROM VIDEO (DO NOT ADD / AT THE END OF PATH)
FACE_IMAGE_FILE_FORMAT = '.png'
FACE_INDEX_FILE_FORMAT = '.txt'

FACE_MATCH_RESULT_CSV_PATH = "output/face_match.csv"
VGG_FACE_MATCH_RESULT_CSV_PATH = "output/face_match_vggface.csv"
FACENET512_MATCH_RESULT_CSV_PATH = "output/face_match_facenet512.csv"


NUMBER_OF_BEST_MATCH_TO_CONSIDER = 5
FAILED_FACE_CAPTURE_CSV_PATH = "output/error/failed_capture_face.csv"

DIRECTORY_OF_INPUT_VIDEO_DIRECTORY = f"{WORKING_DIR_PREFIX}/data-dumps/GWR/downloaded_videos_raw"
# INPUT_VIDEO_DIRECTORY = f"{WORKING_DIR_PREFIX}data-dumps/GWR/new/50" ### DIRECTORY OF VIDEO FILES (DO NOT ADD / AT THE END OF THE PATH) ## unused
INPUT_VIDEO_FILE_FORMAT = '.mp4'

TRANSCRIBED_FILE_PATH = "output/transcribe_text.csv" ### PATH OF THE OUTPUT CSV FILE
USE_FP16 = False

AUDIO_EXTRACT_CSV_PATH = "output/extract_audio_from_video.csv"


FINAL_FACES_DIRECTORY = "output/accepted_video_faces"
FINAL_FACES_CSV_PATH = "output/accepted_video_faces.csv"

INSPECT_DATAFRAME_PATH = f"{WORKING_DIR_PREFIX}/data-dumps/GWR/manual_output/inspect.csv" ### INSPECT.CSV PATH FROM LOCAL MACHINE
MANUAL_FACE_CAPTURE_DIRECTORY = f"{WORKING_DIR_PREFIX}/data-dumps/GWR/manual_output/manual_screenshot_raw" ### DIRECTORY OF MANUALLY CAPTURED FACES(DO NOT ADD "/" AT THE END)

MANUAL_FACE_IMAGE_FILE_FORMAT = ".PNG"
FLATTEN_IMAGE_DIRECTORY = f"{WORKING_DIR_PREFIX}/data-dumps/GWR/manual_output/manual_screenshot_flatten"
FLATTEN_CSV_FILE_PATH = "output/flatten_manual_images.csv"

FLATTEN_ERROR_CSV_FILE_PATH = "output/error/failed_flatten.csv"
# MANUAL_FACE_CAPTURE_DIRECTORY = FLATTEN_IMAGE_DIRECTORY

# INPUT_VIDEO_DIRECTORY = f"{WORKING_DIR_PREFIX}/data-dumps/GWR/input_videos" # TODO: Jay you probably meant DIRECTORY_OF_INPUT_VIDEO_DIRECTORY
FLATTEN_VIDEO_DIRECTORY = f"{WORKING_DIR_PREFIX}/data-dumps/GWR/flattern_input_videos"
VIDEO_FILE_FORMAT =  ".mp4"


FLATTEN_VIDEO_CSV_FILE_PATH =  "output/flatten_input_video.csv"
FLATTEN_VIDEO_ERROR_CSV_FILE_PATH = "output/error/failed_flatten_video.csv"
FINDING_FACE_AGAIN_CSV_PATH = "output/find_faces_again.csv"
FINDING_FACE_AGAIN_ERROR_CSV_PATH = "output/find_faces_again_error.csv"

ADD_IMAGES_TO_API_CSV = "output/add_images_to_api.csv"
ADD_IMAGES_TO_API_ERROR_CSV = "output/error/add_images_to_api_error.csv"

SIMILAR_PLEDGE_TAKERS_API_DIRECTORY = "output/similar_pledge_takers_api"
FIND_FACES_API_CSV = "output/find_faces_api.csv"
FIND_FACES_API_ERROR_CSV = "output/error/find_faces_api_error.csv"
FIND_FACES_MANAGE_PICS_ERROR_CSV = "output/find_faces_manage_pics.csv"

CAPTURE_FACE_BRUT_FORCE_CSV_PATH = "output/capture_face_brut_force.csv"
CAPTURE_FACE_BRUT_FORCE_ERROR_CSV_PATH = "output/error/accepted_pledge_face_not_found.csv"
CAPTURE_FACES_BRUT_FORCE_DIRECTORY = "output/capture_face_brut_force"
CAPTURE_FACES_BRUT_FORCE_ERROR_DIRECTORY = "output/error/accepted_pledge_face_not_found"

FACE_MATCH_ADD_IMAGES_RESPONSE_DIRECTORY = "output/upload/edenai_upload"
FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY = "output/upload/edenai_recognition"

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMjI0NGY2ODMtZTYxNy00MGNkLWFjNTktYjhiZTc5YTQ4NWY1IiwidHlwZSI6ImFwaV90b2tlbiJ9.te2w5Uc3aVbgOylenYlZbnZhxFkXQrvL15p4DB76i3A"