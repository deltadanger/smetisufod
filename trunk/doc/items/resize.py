import os, sys
from PIL import Image

size = 120, 120


for filename in os.listdir("normal"):
    print filename
    infile = os.path.join("normal", filename)
    outfile = os.path.join("small", filename)
    try:
        im = Image.open(infile)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(outfile, "PNG")
    except IOError:
        print "cannot create thumbnail for '%s'" % infile
