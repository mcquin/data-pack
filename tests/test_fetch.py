import hashlib

import pytest
import requests.exceptions
import requests_mock

import datapack.fetch


def test_valid_true():
    content = str.encode("Hello, world!")

    checksum = hashlib.md5(content).hexdigest()

    assert datapack.fetch.valid(content, checksum)


def test_valid_false():
    content = str.encode("Hello, world!")

    checksum = hashlib.md5(str.encode("Hello, test!")).hexdigest()

    assert not datapack.fetch.valid(content, checksum)


def test_fetch_200():
    url = "https://my.cat.says/meow"

    content = str.encode("\x6d\x65\x6f\x77")

    with requests_mock.Mocker() as mock_request:
        mock_request.register_uri("GET", url, content=content, status_code=200)

        assert datapack.fetch.fetch(url) == content


def test_fetch_404():
    url = "https://my.cat.says/quack"

    with requests_mock.Mocker() as mock_request:
        mock_request.register_uri("GET", url, status_code=404)

        with pytest.raises(requests.exceptions.HTTPError):
            datapack.fetch.fetch(url)


def test_fetch_timeout():
    url = "https://my.cat.says/nothing"

    with requests_mock.Mocker() as mock_request:
        mock_request.register_uri("GET", url, exc=requests.exceptions.Timeout)

        with pytest.raises(requests.exceptions.Timeout):
            datapack.fetch.fetch(url)


def test_cache(tmpdir):
    pathname = tmpdir.mkdir("cachedir").join("data.txt")

    content = str.encode("some,new,data")

    datapack.fetch.cache(pathname, content)

    with open(pathname, "rb") as cached:
        assert cached.read() == content


def test_cache_exists(tmpdir):
    pathname = tmpdir.mkdir("cachedir").join("data.txt")

    content = str.encode("some,new,data")

    with open(pathname, "wb") as cached:
        cached.write(str.encode("some,old,data"))

    datapack.fetch.cache(pathname, content)

    with open(pathname, "rb") as cached:
        assert cached.read() == content
