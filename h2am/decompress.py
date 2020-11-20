import zlib
import os

from streamIO import StreamReader
from shared import verify_zlib


def decompressor(data):
    # if data is actually a path
    if type(data) == str:
        data = open(data, "rb").read()

    # create a stream, and store the blam! header for later. (header size = 0x1000)
    stream = StreamReader(data)
    blam_header = stream.read(0x1000)
    
    chunks = []
    # read the header until an empty entry is encountered
    for i in range(0x500):
        size = int.from_bytes(stream.read(4), "little", signed=True)
        if abs(size) > 0:
            # stream.readInt(4) contains offset;                    (size, offset)
            chunks.append((size, stream.readInt(4)))
        else: break;

    # using a file buffer, write the prefix, followed by each decompressed chunk
    with open("tmp", "wb") as file:
        file.write(blam_header)
        # for each chunk, decompress and append to the file
        for i in range(len(chunks) - 1):
            # if chunk size is negative, the chunk is uncompressed
            if chunks[i][0] < 0:
                file.write(data[chunks[i][1] : chunks[i + 1][1]])
                continue
            # if the chunk size is not negative, and not valid zlib. Curropt file
            elif not verify_zlib(data[chunks[i][1] : chunks[i + 1][1]]):
                print("Unable to decompress file: \n\tchunk " + str(i) + " does not contain valid zlib header\n")
                return None
            # chunk size is positive, and it has a valid zlib header. decompress and write to file
            else:
                file.write(zlib.decompress(data[chunks[i][1] : chunks[i][1] + chunks[i][0]]))

    # read back the finalized file
    decompressed_data = open("tmp", "rb").read()

    # remove the file buffer
    os.remove("tmp")

    # return the decompressed data
    return decompressed_data
