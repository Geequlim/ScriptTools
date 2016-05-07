#!/usr/bin/python
# Set it to shaderc absolute path
shaderc = "/home/geequlim/Documents/Workspace/Develop/OpenSource/bgfx/.build/linux64_gcc/bin/shadercDebug"

import os
import sys
import argparse

# Check is the shaderc avaliable
def checkShaderc():
    if os.path.isfile(shaderc):
        return True;
    else:
        print "Error: shaderc doesn\'t exist!\nFile not found:"+shaderc
        return False;

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file",help="The input shaders to compile with")
    parser.add_argument("-i","--include",help="Include path (for multiple paths use semicolon).")
    parser.add_argument("-o","--output",default=".",help="The output directory of the compiled shaders")
    parser.add_argument("-t","--type",type=str, choices=["v", "f", "vertex","fragment"],help="The shader type.")
    parser.add_argument("-var","--varyingdef",help="Path to varying.def.sc file.")
    parser.add_argument("-ct","--compileTarget"
                                            ,type=str,choices=["all","glsl", "gles", "metal","dx9","dx11"],default="all"
                                            ,help="The targets to compiled with.")
    parser.add_argument("-v","--verbose",help="Verbose.")
    return parser.parse_args()

# Setp1 set static command
def getCallCmd(args):
    callCmd = shaderc +" "
    error = None
    if args.file:
        callCmd = callCmd + "-f " + args.file+" "
    else:
        error = "No input file!"
    if args.type:
        callCmd = callCmd + "--type " +args.type+" "
    else:
        error = "Shader type not setted!"
    if args.include:
        callCmd = callCmd + "-i " +args.include+" "
    if args.verbose:
        callCmd = callCmd + "-v "
    if args.varyingdef:
        callCmd = callCmd + "-varyingdef "+args.var
    if error:
        print error;
        return None;
    else:
        return callCmd;

# Step2 set dynamic command and run it
def compile(callCmd,target,args):
    curCmd = callCmd;
    fileName = os.path.splitext(os.path.basename(args.file))[0]+".bin"
    outdir = args.output +"/"+target
    type = args.type;
    if target == "glsl":
        curCmd = curCmd +" --platform linux -p 120 -o "+outdir+"/"+fileName
    elif target == "metal":
        curCmd = curCmd +" --platform osx -p metal -o "+outdir+"/"+fileName
    elif target == "gles":
        curCmd = curCmd +" --platform android -o "+outdir+"/"+fileName
    elif target == "dx9" or target == "dx11":
        curCmd = curCmd +" --platform windows -O 3 "
        if type == "v" or type == "vertex":
            if target == "dx9":
                curCmd = curCmd + " -p vs_3_0 ";
            else:
                curCmd = curCmd + " -p vs_4_0 ";
        else:
            if target == "dx9":
                curCmd = curCmd + " -p ps_3_0 ";
            else:
                curCmd = curCmd + " -p ps_4_0 ";
        curCmd = curCmd + " -o "+outdir+"/"+fileName
    elif target == "all":
        compile(callCmd,"glsl",args)
        compile(callCmd,"gles",args)
        compile(callCmd,"metal",args)
        compile(callCmd,"dx9",args)
        compile(callCmd,"dx11",args)

    if not target == "all":
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        os.system(curCmd)

if __name__ == '__main__':
    args = parseArgs()
    if checkShaderc() :
        callCmd = getCallCmd(args);
        if callCmd:
            compile(callCmd,args.compileTarget,args)
        else:
            print "Error:Bad command :"+callCmd
