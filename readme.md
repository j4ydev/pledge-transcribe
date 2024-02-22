Install python=3.9.6
Install ffmpeg - "brew install ffmpeg"

---

install the following file.
"pip install -r requirement.txt"
"pip install python-Levenshtein"

---

### FOR TRANSCRIBE MODULE

---

Make output directory.
"mkdir output"

---

update line no 16.
run capture_face_img.py file.

---

### FOR FACE MATCHING MODULE

---

create directory screenshots and image_index.
"mkdir screenshots"
"mkdir image_index"

---

update line no 7,8,9.
run capture_face_img.py file.

---

### Instructions

if # comments - It is instructions for code understanding.
if ### comment - Change according to your preference.

---

---

# Work Log

---

Script#1 Get Transcribe and Image Indexes

Phase#1 Base RnD

Phase#2
input:: a directory having videos with file name having metadata - `${pageNumber}_${row}_${column}_${video_id}_${name}`
output::

1. A csv with folllowing columns (do not give header) row, column, index, pageNumber, video-id, transcribed text
2. screenshot, create a file (with same file name as video) in directory named screenshot - that will be used in next step
3. image index, create a file (with same file name as video) in directory named image_index - that will be used later

Phase#3 (TBD)
input:: (a csv or a json that is to be looped)

---

Script#2 Identify potential duplicates

Phase#1 Base RnD

Phase#2
input:: a directory image_index having image hash (one file per video)
output:: CSV file - row, column, index, pageNumber, video-id, video-id:similarity_score, video-id:similarity_score, video-id:similarity_score
Note: o/p csv - column 6, 7, 8 will have top 3 matches in form of video-id:similarity_score, where in the 1st match should always be from itself indicating that with self it is matching 100% :-D

Phase#3 (TBD)
input: (a csv or a json that is to be looped)
output: a csv/json

---

Info: `index: 4 * (row - 1) + column`

---

# High level steps for finding potential duplicate videos

1. input directory FACE_IMAGE_DIRECTORY
2. output file FACE_MATCH_RESULT_CSV_PATH
   1. sample row: 6340954574112, match_found, 6340954574113:difference_indicator, 6340954574114:difference_indicator,
3. image once processed will not be processed again - so check the dataframe before processing
4. output of each face match iteration - a directory inside "output/similar_pledge_takers" - name of directory will be value of corresponding video_id
5. a config variable will specify how many similar faces to list (set it to 5 for now)
6. a config variable will specify the threshhold for difference or similarity
7. the directory thus created will have images in it -
   1. the 1st image should be the one of pledge taker who we are comparing as that face will match the most (assumption)
   2. for example if we are processing 6340954574112_rahul_vp.png
   3. directory name will be 6340954574112
   4. prefix the similarity rank to the file name and store;
   5. example the most matching file will be 1_difference-indicator_6340954574112_rahul_vp.png
   6. where difference_indicator is stringified 1000\*"VGG-Face_cosine" - this should be exact 4 chars, so in case of exact match it will be 1_0000_6340954574112_rahul_vp.png
8. match_found will be set to true if atleast 1 image (except the one corresponding to the self video) is very similar (developer can decide the criteria for that)

---

Transcribe

1. extract_audio_from_video.py
2. audio_transcription.py

Duplicate Face detection - data preparation -- approach #1

1. capture_face_image.py
2. flatten_the_manual_images.py (operators will arrange the data batch wise and we need flattend images for processing, and we need images in png so transform where needed)
3. gather_images.py (from manual screenshots and auto generated screen shots - for the accepted videos gather images having faces
4. flatten_video.py (this we need for the next step)
5. find_faces_again.py (wherever we do not get face from the file gatherd via "gather_images" we reprocess the video to get the face)

Duplicate Face detection - data preparation -- approach #2

1. flatten_video.py
2. capture_face_brut_force.py ( here we mark capture face = yes for all videos irrespective of what we found in capture_face_image)

Duplicate Face detection - process data

1. face_match_facenet512.py
2. face_match_vgg_face.py
3. eden.ai
   1. face_match_add_images.py
   2. face_match_recognition.py
   3.

## DELETE FOLLOWING FILES TO RERUN THE CODE:-

Duplicate Face detection - data preparation

1. "output/capture_face.csv",
   "output/error/failed_capture_face.csv",
   "output/screenshots".

2. "{WORKING_DIR_PREFIX}/data-dumps/GWR/manual_output/manual_screenshot_flatten",
   "output/flatten_manual_images.csv",
   "output/error/failed_flatten.csv"

3. "output/accepted_video_faces",
   "output/accepted_video_faces.csv",
   "output/flatten_manual_images.csv",
   "{WORKING_DIR_PREFIX}/data-dumps/GWR/manual_output/manual_screenshot_flatten"

4. "{WORKING_DIR_PREFIX}/data-dumps/GWR/flattern_input_videos",
   "output/flatten_input_video.csv",
   "output/error/failed_flatten.csv"

5. "output/find_faces_again.csv", "output/find_faces_again_error.csv",

---

face_match_add_images_1.py [ input dir: face_match_add_images_1_input ]
o/p:

- output/upload/edenai_upload_1/ to contain video_id_face_id.json
- face_match_add_images_1.csv
  -- video_id,face_id,image_file_path
  -- 6346229376112,444ddbb0-698b-4c4d-b43a-f74a27afee2f, output/capture_face_brut_force/6346229376112_latif_pathan_brute.png

face_match_recognition_1.py [ input: face_match_add_images_1.csv ]
o/p:

- output/face_match_recognition_1.csv
- vid, face_id, image_file_path, face_id_1, confidence_1, face_id_2, confidence_2, face_id_3, confidence_3
- output/upload/edenai_recognize_1/ to contain video_id_face_id.json
