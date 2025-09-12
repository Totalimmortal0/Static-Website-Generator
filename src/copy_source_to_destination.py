import os
import shutil

# check if destination directory exists, if it does cleans it, if not creates it
if os.path.exists("public"):
    shutil.rmtree("public")
os.mkdir("public")
dest_dir_path = "public"

source_dir_path = "static"

def copy_files(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files(from_path, dest_path)