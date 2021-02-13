import time
import requests

from constatnts import PORT, HOST


def main():
    request_data = {"values": [1, 2, 3]}
    url = f"http://{HOST}:{PORT}/sum"
    ret = requests.get(url, json=request_data).json()["values"]
    print(f"Received: {ret=}")

    request_data = {"values": ret}
    url = f"http://{HOST}:{PORT}/pow"
    ret = requests.get(url, json=request_data).json()["values"]
    print(f"Received: {ret=}")


if __name__ == '__main__':
    start = time.time()
    main()
    stop = time.time()
    print(f'It took: {stop - start} seconds.')
