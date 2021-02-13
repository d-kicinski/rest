import asyncio

import rest
from rest import Message

from example.constatnts import PORT, HOST


@rest.route("/sum")
def route_sum(msg: Message) -> Message:
    return Message([sum(msg.values)])


@rest.route("/pow")
def route_pow(msg: Message) -> Message:
    return Message([pow(v, 2) for v in msg.values])


async def main():
    await rest.serve(HOST, PORT)


if __name__ == '__main__':
    asyncio.run(main())
