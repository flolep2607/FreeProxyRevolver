### This package is not yet published, and not everything outlined in this readme is implemented yet

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

You can also specify to use a fake user agent in requests like this: `pr.get("http://example.com", use_fake_ua=True)`. Websites will often block requests if there is not user agent header, this will take care of that issue for you