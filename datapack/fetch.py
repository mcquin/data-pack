import hashlib


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
