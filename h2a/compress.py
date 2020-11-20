import zlib
import os

from streamIO import StreamReader, StreamWriter


def compressor(data, uncompressed=False):
    # if data is actually a path
    if type(data) == str:
        data = open(data, "rb").read()

    # stream holds all data. header holds offsets and flags
    stream = StreamReader(data)
    header = StreamWriter()

    # chunkify the data into chunks of 8000 bytes
    chunks = []
    while (chunk := stream.read(0x8000)):
        chunks.append(chunk)

    # Open a file to use as a file buffer for the compression
    with open("tmp", "wb") as file:
        # prime the header with chunk count
        header.writeInt(len(chunks))
        # prime the header with flags
        header.writeInt(0x4 if uncompressed else 0x0)
        # first offset
        offset = 0x600000

        for chunk in chunks:
            # write the offset to the header
            header.writeInt64(offset)

            # compress the chunk
            compressed_chunk = chunk if uncompressed else zlib.compress(chunk,level=1)

            # update the offset to include the size of the compressed chunk
            offset += len(compressed_chunk)

            # write the compressed chunk
            file.write(compressed_chunk)

    # the header has a fixed size of 0x600000
    header.write(b'\0' * (0x600000 - header.tell()))

    # read back the file buffer
    with open("tmp", "rb") as file:
        compressed_data = file.read()

    # Remove the file buffer
    os.remove("tmp")

    # Combine the header to the compressed data, and return the entire block
    return header.getvalue() + compressed_data
