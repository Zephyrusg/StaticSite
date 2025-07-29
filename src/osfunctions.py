import os
import shutil

def clear_directory(path, verbose=False):
    if not os.path.exists(path):
        return
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isfile(entry_path) or os.path.islink(entry_path):
            if verbose:
                print(f"Deleting file: {entry_path}")
            os.unlink(entry_path)
        elif os.path.isdir(entry_path):
            clear_directory(entry_path, verbose)
            if verbose:
                print(f"Deleting directory: {entry_path}")
            os.rmdir(entry_path)

def copy_directory(src, dst, verbose=False):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        dst_path = os.path.join(dst, entry)
        if os.path.isdir(src_path):
            copy_directory(src_path, dst_path, verbose)
        else:
            if verbose:
                print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy2(src_path, dst_path)

def copy_static_to_public(src, dst, verbose=False):
    clear_directory(dst, verbose)
    if not os.path.exists(dst):
        os.makedirs(dst)
    copy_directory(src, dst, verbose)
