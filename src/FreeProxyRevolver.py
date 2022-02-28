import requests
from requests import request
import FreeProxyScraper
from FreeProxyScraper import Proxy
from typing import Callable, Iterator, Union
from fake_useragent import UserAgent
import threading
import time
from fp.fp import FreeProxy
ua = UserAgent()

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
        #self.proxies = scrape_loop(**kwargs)
        self.proxies = self.loop()
        self.working=[]
        self.broken=[]
        t=threading.Thread(target=self.gen1)
        t.start()
        p=threading.Thread(target=self.gen2)
        p.start()
        self.current_proxy = next(self.proxies)
    def loop(self):
        while True:
            for p in self.working:
                yield p
            time.sleep(0.2)
    def rotate_proxy(self):
        self.current_proxy = next(self.proxies)
    def checker(self,address):
        try:
            if address not in self.working and address not in self.broken:
                #print("test:",address,len(self.working))
                rep=requests.get("http://httpbin.org/status/200",proxies={"http": address,"https": address},timeout=5)
                #print("saint test")
                if rep.status_code==200:
                    rep=requests.get("http://api.jeuxvideo.com/forums/42-51-69077786-1-0-1-0-m6-enquete-exclusive-invasion-de-l-ukraine-poutine-declare-la-guerre-au-monde.htm",proxies={"http": address,"https": address},timeout=5) 
                    if rep.status_code==200:
                        self.working.append(address)
        except Exception as e:
            #print(">>",e)
            self.broken.append(address)
    def gen1(self):
        while True:
            pq = FreeProxyScraper.ProxyQuery()
            for proxy in pq.find_filter():
                if not proxy:break
                #print("new prox",proxy.address)
                self.checker(proxy.address)
    def gen2(self):
        while True:
            proxies = FreeProxy()
            address=proxies.get()
            while address:
                self.checker(address)
                address=proxies.get()
                
    def make_request(self, method: str, *args, use_fake_ua: bool =False, **kwargs) -> Union[None, requests.Response]:
        for rotation in range(self.max_rotates):
            kwargs["proxies"] = {"http": self.current_proxy,"https": self.current_proxy}
            if use_fake_ua:
                if "headers" not in kwargs:
                    kwargs["headers"] = {}
                kwargs["headers"]["User-Agent"] = ua.random

            try:
                response = request(method, *args, **kwargs)
            except Exception as e:
                print(e)
                print(self.current_proxy)
                response = None
                self.rotate_proxy()
                continue

            if response.status_code in self.rotate_on_code:
                print("bruu",response.status_code)
                self.rotate_proxy()
                continue

            if len(self.rotate_not_on_code) > 0 and response.status_code not in self.rotate_not_on_code:
                print("bl",response.status_code)
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

