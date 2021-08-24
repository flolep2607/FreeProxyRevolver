### This package is not yet published, and not everything outlined in this readme is implemented yet

# FreeProxyRevolver
This package provides an abstraction layer over the requests library which automatically routes your requests through proxies, automatically revolving to the next proxy when requests become unsuccessful through it

## Installation
```shell
pip3 install FreeProxyRevolver
```

## Usage
```python
import FreeProxyRevolver

pr = FreeProxyRevolver.scrape_revolver()

# Use just like requests
pr.get("http://example.com", json={"my": "data"})
```
