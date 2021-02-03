import sys
import os

from h1a import *
from h2a import *
from h2am import *


def init_QuiCript():
    # verify we have enough arguments
    if len(sys.argv) < 4:
        print("QuiCript 'h1a'/'h2a'/'h2am' -c/-d 'path/to/file' ... 'path/to/third/file' ")
        return

    # get arguments
    compression_type = sys.argv[1]
    compress = sys.argv[2]
    paths = sys.argv[3:]

    # Do not continue until correct compression type detected
    if compression_type not in ["h1a", "h2a", "h2am"]:
        print("Unable to determine compression type: \n\th1a\n\th2a\n\n\th2am\n\ncompression type >")
        return

    if compress not in ["-d", "-c"]:
        print("Unable to determine desired action: \n\t-c\tcompress\n\t-d\tdecompress")
        return

    for file in paths:
        # if it is actually a folder pass until file
        if os.path.isdir(file):
            continue

        # read data
        data = open(file, "rb").read()

        # Lost verify_compression somewhere in translation
        #if compress == "-d":
        #    if not verify_compression(data, compression_type):
        #        print("File failed integrity test")
        #        break

        if compression_type == "h1a":
            if compress == "-c":
                print("Compressing: " + file.split("/")[-1] + " with h1a compression")
                open(file + "_tmp", "wb").write(h1a_compress(data))
                os.remove(file) #save to a temp file as to not overwrite original if failed
                os.rename(file + "_tmp", file)
            if compress == "-d":
                print("Decompressing: " + file.split("/")[-1] + " with h1a compression")
                open(file + "_tmp", "wb").write(h1a_decompress(data))
                os.remove(file)
                os.rename(file + "_tmp", file)
                
        
        elif compression_type == "h2a":
            if compress == "-c":
                print("Compressing: " + file.split("/")[-1] + " with h2a compression")
                open(file + "_tmp", "wb").write(h2a_compress(data))
                os.remove(file)
                os.rename(file + "_tmp", file)
            if compress == "-d":
                print("Decompressing: " + file.split("/")[-1] + " with h2a compression")
                open(file + "_tmp", "wb").write(h2a_decompress(data))
                os.remove(file)
                os.rename(file + "_tmp", file)
                
                
        elif compression_type == "h2am":
            if compress == "-c":
                print("Compressing: " + file.split("/")[-1] + " with h2a compression")
                open(file + "_tmp", "wb").write(h2am_compress(data))
                os.remove(file)
                os.rename(file + "_tmp", file)
            if compress == "-d":
                print("Decompressing: " + file.split("/")[-1] + " with h2am compression")
                open(file + "_tmp", "wb").write(h2am_decompress(data))
                os.remove(file)
                os.rename(file + "_tmp", file)

init_QuiCript()
