try:
    from urllib.parse import urlunparse, urlparse, urlencode
except ImportError:
    from urlparse import urlparse, urlunparse
    from urllib import urlencode


def make_url(url, qs):
    url_parts = list(urlparse(url))
    url_parts[4] = urlencode(qs)
    u = urlunparse(url_parts)
    return u
