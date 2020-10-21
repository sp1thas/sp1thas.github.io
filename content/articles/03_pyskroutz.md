Title: pyskroutz
Date: 2018-07-18 18:40
Modified: 2018-07-18 18:40
Tags: python
Category: blog
Slug: pyskroutz
Author: Panagiotis Simakis
Summary: Unofficial Python SDK for Skroutz.gr API.

Unofficial Python SDK for Skroutz.gr API

![Pypi](https://img.shields.io/pypi/v/pySkroutz.svg)

This client library is designed to support the Skroutz API. You can read more about the Skroutz API by accessing its official documentation.

## Install

via PyPI:

```
$ pip install pySkroutz
```

## Usage

```
>>> from pySkroutz import Skroutz
>>> client_id = 'your client id'
>>> client_secret = 'your client secret'
>>> skrtz = Skroutz(client_id=client_id, client_secret=client_secret)
>>> skrtz.search('xiaomi redmi note 4')
```

## License

This project is licensed under the GNU General Public License version 3
