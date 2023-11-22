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
