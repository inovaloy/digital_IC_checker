import os

def isFile(path):
    mode = os.stat(path)[0]
    if mode & 0x8000:  # Regular file
        return True
    return False


def isFolder(path):
    mode = os.stat(path)[0]
    if mode & 0x4000:  # Directory
            return True
    return False
