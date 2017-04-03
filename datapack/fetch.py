import hashlib

import requests


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
