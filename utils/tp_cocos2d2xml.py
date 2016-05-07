#!/usr/bin/python

import plistlib
import re
import sys
import os


def conver(path):
    pl = plistlib.readPlist(path)
    # pl = plistlib.readPlist("S052_stand.plist")
    texfile = pl["metadata"]["textureFileName"]
    xmlContent = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Created with TexturePacker http://www.codeandweb.com/texturepacker-->
<!-- {} -->
<!--Format:
n  => name of the sprite
x  => sprite x pos in texture
y  => sprite y pos in texture
w  => sprite width (may be trimmed)
h  => sprite height (may be trimmed)
pX => x pos of the pivot point (relative to sprite width)
pY => y pos of the pivot point (relative to sprite height)
oX => sprite's x-corner offset (only available if trimmed)
oY => sprite's y-corner offset (only available if trimmed)
oW => sprite's original width (only available if trimmed)
oH => sprite's original height (only available if trimmed)
r => 'y' only set if sprite is rotated
-->
<TextureAtlas imagePath="{}" width="{}" height="{}">
"""
    m = pl["metadata"]
    texSize = re.findall(re.compile("{(\d+),(\d+)}"), m["size"])[0]
    xmlContent = xmlContent.format(
        m["smartupdate"], m["textureFileName"], texSize[0], texSize[1])

    spriteLine = '    <sprite n="{}" x="{}" y="{}" w="{}" h="{}" pX="0" pY="0" oX="{}" oY="{}" oW="{}" oH="{}" {}/>\n'
    for f in pl["frames"].keys():
        n = f
        f = pl["frames"][f]
        frame = re.findall(re.compile("{{(\d+),(\d+)},{(\d+),(\d+)}}"), f["frame"])[0]
        of = re.findall(re.compile("{{(\d+),(\d+)},{(\d+),(\d+)}}"), f["sourceColorRect"])[0]
        rotate = f["rotated"] and 'r="y"' or ''
        xmlContent += spriteLine.format(n, frame[0], frame[1], frame[2], frame[3], of[0], of[1], of[2], of[3], rotate)
    xmlContent += "</TextureAtlas>\n"
    return xmlContent

if __name__ == '__main__':
    xml = conver(sys.argv[1])
    file = open(sys.argv[2], 'w+')
    file.write(xml)
    file.flush()
    file.close()
