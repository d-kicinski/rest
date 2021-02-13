# rest

The simplest api for creating web interface to your functions.
* no external dependencies :heavy_check_mark:
* no batteries included :heavy_check_mark:
* barely works :fire: :heavy_check_mark: :fire:


```python
import asyncio

import rest
from rest import Message


@rest.route("/sum")
def route_sum(msg: Message) -> Message:
    return Message([sum(msg.values)])


@rest.route("/pow")
def route_pow(msg: Message) -> Message:
    return Message([pow(v, 2) for v in msg.values])


async def main():
    await rest.serve("127.0.0.1", 8888)


if __name__ == '__main__':
    asyncio.run(main())
```
