# coding=utf-8
import fnmatch
import os
import glob


def globPath(path, pattern):
    result = []
    for root, subdirs, files in os.walk(path):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                result.append(os.path.join(root, filename))
    return result


def search(pattern, dirOnly=False):
    files = []
    path = os.path.dirname(pattern)
    patternValue = os.path.basename(pattern)
    if patternValue.count("**"):
        files = globPath(path, patternValue)
    else:
        files = glob.glob(pattern)
    if dirOnly:
        dirs = []
        for path in files:
            if os.path.isdir(path):
                dirs.append(path)
        return dirs
    else:
        return files
