import hashlib

import datapack.fetch


def test_valid_true():
    content = str.encode("Hello, world!")

    checksum = hashlib.md5(content).hexdigest()

    assert datapack.fetch.valid(content, checksum)


def test_valid_false():
    content = str.encode("Hello, world!")

    checksum = hashlib.md5(str.encode("Hello, test!")).hexdigest()

    assert not datapack.fetch.valid(content, checksum)
