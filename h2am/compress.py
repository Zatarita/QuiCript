import zlib
import os

from streamIO import StreamReader, StreamWriter


def compressor(data):
	# if data is actually a path
	if type(data) == str:
		data = open(data, "rb").read()

	# stream holds all data. header holds offsets, and chunk sizes, blam! header stays uncompressed.
	stream = StreamReader(data)
	header = StreamWriter()
	blam_header = stream.read(0x1000)

	# chunkify the data into blobs of 0x40000 bytes
	chunks = []
	while (chunk := stream.read(0x40000)):
		chunks.append(chunk)

	# Open a file to use as a file buffer for the compression
	with open("tmp", "wb") as file:
		# first offset
		offset = 0x3000
		# write blam! header
		header.write(blam_header)

		# for each chunk
		for chunk in chunks:
			# compress the chunk and store the chunk size
			compressed_chunk = zlib.compress(chunk, 4)
			chunk_size = len(compressed_chunk)

			# write the chunk size to the header
			header.writeInt(chunk_size)
			# write the offset to the header
			header.writeInt(offset)

			# calculate and apply alignment padding
			# the sum of the chunk size and offset will tell us our current position in the file.
			# divide the current position by the alignment (0x80). If we drop the decimal
			# and add one to the result we will get an offset that matches our block alignment, and is also
			# large enough to contain the data from the compressed chunk.
			offset = int((chunk_size + offset) / 0x80)
			offset = (offset + 1) * 0x80

			local_offset = int((chunk_size + file.tell()) / 0x80)
			local_offset = (local_offset + 1) * 0x80
			
			# write the compressed chunk
			file.write(compressed_chunk)
			# seek to the next alignment
			file.seek(local_offset)


	# the header has a fixed size of 0x3000; fill in padding
	header.write(b'\0' * (0x3000 - header.tell()))

	# read back the file buffer
	with open("tmp", "rb") as file:
		compressed_data = file.read()

	# Remove the file buffer
	# os.remove("tmp")

	# Combine the header to the compressed data, and return the entire block
	return header.getvalue() + compressed_data
