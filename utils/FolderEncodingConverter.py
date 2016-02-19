#!/usr/bin/python
# coding=utf-8
import fnmatch
import os
import chardet
import argparse


def globPath(path, pattern):
    result = []
    for root, subdirs, files in os.walk(path):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                result.append(os.path.join(root, filename))
    return result


def to_encoding(buf, encode, ignoreBelow=0.7):
    '''
    Convert encode the string buffer
    '''
    result = [buf, False]
    try:
        charInfo = chardet.detect(buf)
        if (charInfo['confidence'] >= ignoreBelow):
            result[0] = (buf.decode(charInfo['encoding'])).encode(encode)
            result[1] = True
        else:
            raise Exception('Cannot convert encoding with small precision!')
    except Exception as e:
        print e.message
    return result[0], result[1]


def convert_files(indir, outdir, encode):
    try:
        files = globPath(indir, '**')
        counter = [0.0]
        for file in files:
            outPath = outdir + file[len(indir):]
            filedir = os.path.dirname(outPath)
            if not os.path.isdir(filedir):
                try:
                    os.makedirs(filedir)
                except Exception as e:
                    print e.message
                    continue
            res = to_encoding(open(file, 'r').read(), encode)[0]
            ofile = open(outPath, 'w+')
            ofile.write(res)
            ofile.flush()
            ofile.close()
            counter[0] += 1.0
            percent = counter[0] / len(files) * 100
            print '[%.1f%%|%d/%d] %s => %s' % (percent, counter[0], len(files), file, outPath)
    except Exception as e:
        print e.message

cliParser = argparse.ArgumentParser(
    "Convert all file under input directory's encoding")
cliParser.add_argument("-i",
                       "--input",
                       default=None,
                       help="The directory path to load file with")
cliParser.add_argument("-o",
                       "--output",
                       default=None,
                       help="""
                       The directory path to save files converted
                       Defualt to over write input files
                       """)
cliParser.add_argument("-c",
                       "--encode",
                       default='utf-8',
                       help="The encoding convert to, default = utf-8")
args = cliParser.parse_args()

if __name__ == '__main__':
    inputDir = args.input
    if inputDir:
        outdir = args.output
        if not outdir:
            outdir = inputDir
        convert_files(inputDir, outdir, args.encode)
    else:
        print "Please set input directory!"
