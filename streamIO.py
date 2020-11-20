from io import BytesIO
from struct import pack


class StreamReader(BytesIO):
    def __init__(self, data):
        BytesIO.__init__(self, data)

    # return an int of specified length from the byte stream
    def readInt(self, length: int):
        return int.from_bytes(self.read(length), "little")

    def readInt32(self):
        return int.from_bytes(self.read(4), "little")

    def readInt64(self):
        return int.from_bytes(self.read(8), "little")

    # read either a null terminated string, or a set size string
    def readString(self, encoding="utf-8", null_terminated=True, length=-1):
        # a string of zero bytes is possible. If that is the case, return nothing
        if not length:
            return
        # if a length is specified, the string is not null terminated
        if length > 0:
            null_terminated = False

        # if the string is null terminated (DEFAULT)
        if null_terminated:
            # create a buffer to hold the characters
            string_builder = ""
            # get the first character in the stream
            char_buffer = self.read(1).decode(encoding)

            # repeat until we receive null character reached
            while char_buffer != '\0':
                # Append the character from the stream to the string buffer
                string_builder += char_buffer
                # read the next character
                char_buffer = self.read(1).decode(encoding)

            # once complete, return the created string.
            return string_builder
        # if the string is of set length
        else:
            if length >= 0:
                # if a length is specified just read the block, and decode it.
                test = self.tell()
                return self.read(length).decode(encoding)

    # burn padding of set length
    def burn(self, length):
        self.read(length)


class StreamWriter(BytesIO):
    def __init__(self, endian="<"):
        BytesIO.__init__(self)
        # endianess of the file write
        self.endian = endian

    # Write an integer to the stream
    def writeInt(self, data: int):
        self.write(pack(self.endian + "I", data))

    def writeInt64(self, data: int):
        self.write(pack(self.endian + "Q", data))

    def writeSInt64(self, data: int):
        self.write(pack(self.endian + "q", data))

    # Write a string to the stream
    def writeString(self, string, encoding="utf-8"):
        if not string:
            return
        self.write(string.encode(encoding))
