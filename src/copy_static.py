import os
import shutil


def copy_directory(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for filename in os.listdir(src):
        src_path = os.path.join(src, filename)
        dst_path = os.path.join(dst, filename)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_directory(src_path, dst_path)
