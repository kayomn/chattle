import sys
import json
import struct


class Message:
    def __init__(self, author: str, body: str) -> None:
        self.author = author
        self.body = body

    def serialize(self) -> bytes:
        return serialize(self.author, self.body)


def deserialize(data: bytes) -> Message:
    buffer_length = 2
    header_length = struct.unpack(">H", data[:buffer_length])[0]
    header = json.loads(data[buffer_length:header_length])

    return Message(header["author"], header["encoded-body"])


def serialize(author: str, body: str) -> bytes:
    encoding = sys.getdefaultencoding()

    header_bytes = json.dumps({
        "byteorder": sys.byteorder,
        "author": author,
        "body": encoding,
    }).encode("utf-8")

    return (struct.pack(">H", len(header_bytes)) + header_bytes)