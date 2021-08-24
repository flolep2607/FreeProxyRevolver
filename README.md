# FreeProxyRevolver
This package provides implements requests library and automatically routes your requests through proxies, automatically revolving to the next proxy when requests become unsuccessful through it

## Installation
```shell
pip3 install FreeProxyRevolver
```

## Usage
```python
import FreeProxyRevolver

pr = FreeProxyRevolver.Revolver()

# Use just like requests
response = pr.get("http://example.com")
print(response.content)
```

You can also specify to use a fake user agent in requests like this: `pr.get("http://example.com", use_fake_ua=True)`. Websites will often block requests if there is not a user agent header, this will take care of that issue for you

`FreeProxyRevolver.Revolver()` also has a couple of parameters you can set in order to configure it. Here's a list of them all:

parameter         | purpose
------------------|-----------------------------------------------------------------------------------
rotate_on_code    | A list of http response codes that should trigger a rotation of which proxy is used. Default: `[429, 403]`
rotate_not_on_code| A list of http response codes that should trigger a rotation of which proxy is used if the returned code is **not** on the list. Default: `[429, 403]`
max_rotates       | The maximum proxy rotations that should be tried before giving up on rotating proxies and just returning whatever was retrieved, regardless of response code. Default: `6`