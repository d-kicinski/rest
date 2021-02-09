from __future__ import annotations

import asyncio
import dataclasses
import json
from asyncio import StreamReader, StreamWriter
from dataclasses import dataclass
from typing import List, Dict

from constatnts import HOST, PORT


RESPONSE = "HTTP/1.1 {status} {status_msg}\r\n" \
           "Content-Type: application / json\r\n" \
           "Content-Encoding: UTF-8\r\n" \
           "Accept-Ranges: bytes\r\n" \
           "Connection: closed\r\n" \
           "\r\n" \
           "{json}"


@dataclass
class Message:
    values: List[float]

    @staticmethod
    def form_json(json_str: str) -> Message:
        json_dict = json.loads(json_str)
        return Message(json_dict["values"])

    def json(self) -> Dict:
        return dataclasses.asdict(self)

    def __str__(self):
        return f'{{"values": {self.values}}}'


@dataclass
class HTMLHeader:
    method: str
    url: str
    host: str
    connection: str
    content_length: int


def route_sum(msg: Message) -> Message:
    return Message([sum(msg.values)])


def route_pow(msg: Message) -> Message:
    return Message([pow(v, 2) for v in msg.values])


ROUTES = {
    "/sum": route_sum,
    "/pow": route_pow
}


def build_response(header: HTMLHeader, data: Message) -> bytes:
    response = RESPONSE.format(
        status=200,
        status_msg="OK",
        json=str(data)
    ).encode('utf-8')

    return response


def parse_header(header: str) -> HTMLHeader:
    http_lines = header.split('\r\n')
    method, url, _ = http_lines[0].split(' ')
    host = http_lines[1].strip().split(' ')[1]
    connection = http_lines[5].split(' ')[1]
    content_length = http_lines[6].split(' ')[1]
    return HTMLHeader(method, url, host, connection, int(content_length))


async def read_html_header(reader: StreamReader) -> HTMLHeader:
    header_str = ""
    while True:
        header_bytes: bytes = await reader.readline()
        if header_bytes == b'\r\n':
            break
        header_str += header_bytes.decode()

    print(header_str)
    return parse_header(header_str)


async def read_message(reader: StreamReader, message_length: int) -> Message:
    content_bytes = await reader.read(message_length)
    return Message.form_json(content_bytes.decode())


async def handle_client(reader: StreamReader, writer: StreamWriter):
    header: HTMLHeader = await read_html_header(reader)
    message: Message = await read_message(reader, header.content_length)

    print(header)

    ret: Message = ROUTES[header.url](message)

    response: bytes = build_response(header, ret)

    writer.write(response)
    await writer.drain()

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client,
                                        host=HOST, port=PORT, reuse_address=True, reuse_port=True,
                                        start_serving=False)
    await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
