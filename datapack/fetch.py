import hashlib
import os.path

import requests


def cache(pathname, content):
    """
    Save content to a file.

    :param pathname: Cache content at this location. Pre-existing content is overwritten.
    :type pathname: str

    :param content: Data to cache.
    :type content: bytes
    """
    with open(pathname, "wb") as cache_file:
        cache_file.write(content)


def fetch(url):
    """
    Retrieve data from a URL.

    :rtype: bytes

    :param url: The URL to get data from.
    :type url: str

    :return: Data (as bytes) retrieved from the URL.
    """
    response = requests.get(url, timeout=10)

    if response.ok:
        return response.content

    response.raise_for_status()


def has_cached_copy(pathname, checksum):
    """
    Verify cached content with a checksum.

    :rtype: bool

    :param pathname: Location of cached content on the filesystem.
    :type pathname: str

    :param checksum: Expected hexadecimal string digest of cached content.
    :type checksum: str

    :return: True if the checksum of the cached content matches the provided checksum
    """
    if not os.path.exists(pathname):
        return False

    with open(pathname, "rb") as cache_file:
        return valid(cache_file.read(), checksum)


def valid(content, checksum):
    """
    Validate content with a precomputed MD5 checksum.

    :rtype: bool
    
    :param content: Data to compare against checksum.
    :type content: bytes

    :param checksum: Expected hexadecimal string digest of content.
    :type checksum: str

    :return: True if the checksum generated from content matches checksum.
    """
    return hashlib.md5(content).hexdigest() == checksum
