import struct
import zlib
import os

from streamIO import StreamReader, StreamWriter


def compressor(data):
    # if data is actually a path
    if type(data) == str:
        data = open(data, "rb").read()

    # stream holds all data. header holds offsets
    stream = StreamReader(data)
    header = StreamWriter()

    # chunkify the data into chunks of 0x20000 bytes
    chunks = []
    while (chunk := stream.read(0x20000)):
        chunks.append(chunk)

    # Open a file to use as a file buffer for the compression
    with open("tmp", "wb") as file:
        # prime the header with chunk count
        header.writeInt(len(chunks))
        # first offset
        offset = (len(chunks) * 4) + 4
        
        # for each chunk
        for chunk in chunks:
            # write the offset to the header
            header.writeInt(offset)

            # compress the chunk
            compressed_chunk = zlib.compress(chunk, 4)

            # update the offset to include the size of the compressed chunk
            offset += len(compressed_chunk) + 4

            # write the compressed chunk size, and the compressed chunk
            file.write(struct.pack("<I", len(chunk)))
            file.write(compressed_chunk)

    # read back the file buffer
    with open("tmp", "rb") as file:
        compressed_data = file.read()

    # Remove the file buffer
    os.remove("tmp")

    # Combine the header to the compressed data, and return the entire block
    return header.getvalue() + compressed_data
