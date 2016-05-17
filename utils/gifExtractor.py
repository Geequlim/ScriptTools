#!/usr/sbin/python

import os
import sys
from PIL import Image


def extractFrames(inGif, outFolder):
    frame = Image.open(inGif)
    f = 0
    while frame:
        frame.save('%s/%s_%s.png' %
                   (outFolder, os.path.basename(inGif), f), 'PNG')
        f += 1
        try:
            frame.seek(f)
        except EOFError:
            break
    return True


if __name__ == '__main__':
    try:
        if not os.path.isdir(sys.argv[2]):
            os.makedirs(sys.argv[2])
        extractFrames(sys.argv[1], sys.argv[2])
    except Exception as e:
        print(e.message)
