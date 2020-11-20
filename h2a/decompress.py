import zlib
import os

from streamIO import StreamReader
from shared import verify_zlib


def decompressor(data):
    # if data is actually a path
    if type(data) == str:
        data = open(data, "rb").read()

    # stream holds all data. chunk count, and uncompressed flag
    stream = StreamReader(data)
    count = stream.readInt(4)
    uncompressed_flag = stream.readInt(4)

    # read the offsets from the stream. Store file length as pseudo "last offset"
    offsets = [stream.readInt(8) for i in range(count)]
    offsets.append(len(data))

    # using a file buffer
    with open("tmp", "wb") as file:
        # for each offset
        for i in range(len(offsets) - 1):
            # if the uncompressed flag is set
            if uncompressed_flag:
                # copy the data
                decomp = data[offsets[i] : offsets[i + 1]]
            # if the uncompressed flag is not set
            else:
                # if a zlib header couldn't be identified
                if not verify_zlib(data[offsets[i] : offsets[i + 1]]):
                    print("Unable to decompress file: \n\tchunk " + str(i) + " does not contain valid zlib header\n")
                    return None
                # decompress the data
                decomp = zlib.decompress(data[offsets[i] : offsets[i + 1]])
            # write to file buffer
            file.write(decomp)

    # read back the file buffer
    decompressed_data = open("tmp", "rb").read()

    # clean up the temp file
    os.remove("tmp")

    # return the decompressed data
    return decompressed_data
