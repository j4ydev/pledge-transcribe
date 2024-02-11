import glob
import os

### Handled cases:
# 1. when there is vid_fname_lname.png file. We will not rename the file.
# 2. when there is vid_frame_lname_.png file. We will not rename the file.
# 3. when there is id_vid_fname_lname.png file. rename to make it vid_fname_lname.png
# 4. When there is id_vid_{dr/ms/mr}_fname_lname.png file. rename to make vid_{dr/ms/mr}_fname_lname.png

# TO ADD 1 LAYER OF ASSURANCE:: before removing any id it will check if id term is int or not if not then we will not remove the id term.

#
screenshot_image_list = glob.glob("/Users/khasgiwa/Workbench/codebench/a7v/pledge-transcribe/output/screenshots/*.png") ## update the location of screenshot directory.
print(screenshot_image_list[0])

for image_path in screenshot_image_list:
    image_name = image_path.split("/")[-1].replace(".png", "")

    image_name_naming_convention_elements_list = image_name.split("_")

    if "" in image_name_naming_convention_elements_list:
        image_name_naming_convention_elements_list.remove("")

    print(image_name_naming_convention_elements_list)

    if len(image_name_naming_convention_elements_list) >= 4:
        print(f"{image_name_naming_convention_elements_list[0]}_")

        if float(image_name_naming_convention_elements_list[0]):
            new_rename_image_path = image_path.replace(f"{image_name_naming_convention_elements_list[0]}_", "")
            print(new_rename_image_path)

            os.rename(image_path, new_rename_image_path)


