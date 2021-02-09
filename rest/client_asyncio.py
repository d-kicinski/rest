import time
import requests

from aiohttp import ClientSession

from constatnts import PORT, HOST



async def hello(fetch_url):
    async with ClientSession() as session:
        async with session.post(fetch_url, json=request_data) as response:
            print(await response.json())
            print("Waiting for response")
            print(await response.text())
            response.close()


def main():
    # loop = asyncio.get_event_loop()
    #
    # tasks = []
    #

    request_data = {"values": [1, 2, 3]}
    url = f"http://{HOST}:{PORT}/sum"
    ret = requests.get(url, json=request_data).json()["values"]
    print(f"Received: {ret=}")

    request_data = {"values": ret}
    url = f"http://{HOST}:{PORT}/pow"
    ret = requests.get(url, json=request_data).json()["values"]
    print(f"Received: {ret=}")

    # task = asyncio.ensure_future(hello(url))
    # tasks.append(task)
    # loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    start = time.time()
    main()
    stop = time.time()
    print(f'It took: {stop - start} seconds.')
