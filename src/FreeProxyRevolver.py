import requests
from requests import request
import FreeProxyScraper
from FreeProxyScraper import Proxy
from typing import Callable, Iterator, Union
from fake_useragent import UserAgent


ua = UserAgent()


def scrape_loop(*args, **kwargs) -> Iterator[Proxy]:
    while True:
        pq = FreeProxyScraper.ProxyQuery()
        for proxy in pq.find_filter(*args, **kwargs):
            yield proxy


class Revolver:
    def __init__(self, rotate_on_code: list =None, rotate_not_on_code: list =None, max_rotates: int=6, **kwargs):
        assert max_rotates >= 0, "Rotations must be 0 or a positive integer"

        if rotate_not_on_code is None:
            rotate_not_on_code = []

        if rotate_on_code is None:
            rotate_on_code = [429, 403]

        self.rotate_not_on_code = rotate_not_on_code
        self.rotate_on_code = rotate_on_code
        self.max_rotates = max_rotates
        self.proxies = scrape_loop(**kwargs)
        self.current_proxy = next(self.proxies)

    def rotate_proxy(self):
        self.current_proxy = next(self.proxies)

    def make_request(self, method: str, *args, use_fake_ua: bool =False, **kwargs) -> Union[None, requests.Response]:
        for rotation in range(self.max_rotates):
            kwargs["proxies"] = {"http": self.current_proxy.address,"https": self.current_proxy.address}
            if use_fake_ua:
                if "headers" not in kwargs:
                    kwargs["headers"] = {}
                kwargs["headers"]["User-Agent"] = ua.random

            try:
                response = request(method, *args, **kwargs)
            except Exception as e:
                print(e)
                response = None
                self.rotate_proxy()
                continue

            if response.status_code in self.rotate_on_code:
                self.rotate_proxy()
                continue

            if len(self.rotate_not_on_code) > 0 and response.status_code not in self.rotate_not_on_code:
                self.rotate_proxy()
                continue

            return response
        return response

    def get(self, *args, **kwargs) -> Union[None, requests.Response]:
        return self.make_request("get", *args, **kwargs)

    def head(self, *args, **kwargs) -> Union[None, requests.Response]:
        return self.make_request("head", *args, **kwargs)

    def post(self, *args, **kwargs) -> Union[None, requests.Response]:
        return self.make_request("post", *args, **kwargs)

    def patch(self, *args, **kwargs) -> Union[None, requests.Response]:
        return self.make_request("patch", *args, **kwargs)

    def put(self, *args, **kwargs) -> Union[None, requests.Response]:
        return self.make_request("put", *args, **kwargs)

    def delete(self, *args, **kwargs) -> Union[None, requests.Response]:
        return self.make_request("delete", *args, **kwargs)

    def options(self, *args, **kwargs) -> Union[None, requests.Response]:
        return self.make_request("options", *args, **kwargs)
