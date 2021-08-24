from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="FreeProxyRevolver",
    version="0.0.1",
    description="a package that allows you to automatically revolve your http requests through various proxies",
    py_modules=["FreeProxyRevolver"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests[socks]",
        "FreeProxyScraper",
        "fake-useragent"
    ],
    extras_require={
        "dev": [
            "pytest"
        ]
    },
    url="https://github.com/Themis3000/FreeProxyRevolver",
    author="Themi Megas",
    author_email="tcm4760@gmail.com"
)
