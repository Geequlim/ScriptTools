#!/usr/bin/python
# coding=utf-8
import os
import argparse
from encodingConverter import to_encoding
from path import globPath


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


cliParser = argparse.ArgumentParser("Convert all file under input directory's encoding")
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
