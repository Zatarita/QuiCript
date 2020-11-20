import zlib
import os

from streamIO import StreamReader
from shared import verify_zlib


def decompressor(data):
    # if data is actually a path
    if type(data) == str:
        data = open(data, "rb").read()


    # stream holds all data. chunk count
    stream = StreamReader(data)
    count = stream.readInt(4)

    # read the offsets from the stream. Store file length as pseudo "last offset"
    offsets = [stream.readInt(4) + 4 for i in range(count)]
    offsets.append(len(data))

    # using a file buffer
    with open("tmp", "wb") as file:
        # for each chunk
        for i in range(len(offsets) - 1):
            # if a valid zlib header wasn't found
            if not verify_zlib(data[offsets[i]:offsets[i + 1]]):
                print("Unable to decompress file: \n\tchunk " + str(i) + " does not contain valid zlib header\n")
                return None
            # decompress the chunk
            file.write(zlib.decompress(data[offsets[i]:offsets[i + 1]]))

    # read the buffer back
    with open("tmp", "rb") as file:
        decompressed_data = file.read()

    # cleanup
    os.remove("tmp")

    # return decompressed data
    return decompressed_data
