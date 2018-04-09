import re

from marshmallow import ValidationError
from pygmy.config import config
from urllib.parse import urljoin, urlparse, parse_qs, urlunparse, urlencode


def validate_url(url):
    """Simple URL validator."""
    url = url or 'invalid'
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    is_valid = regex.match(url) is not None
    if is_valid:
        url = urlparse(url)
        # TODO
        allowed_path = ['contact', 'about', 'shorten', 'dashboard']
        if url.netloc == 'pygy.co' and url.path.strip('/') not in allowed_path:
            raise ValidationError('URL is already a pygmy shortened link.')
    return is_valid


def make_short_url(short_path):
    short_url = urljoin(
        config.pygmy['short_url_schema'],
        config.pygmy['short_url'],
        short_path)
    return short_url


def get_short_path(short_url):
    parts = urlparse(short_url)
    short_path = parts.path.lstrip('/')
    return short_path


def set_url_macro(url, ext_data):
    """
    Add macro data in url args.
    Such as: 'http://www.google.com/' will return 'http://www.google.com/?'

    :param ext_data: bilin ext_data
    :return: new_url, str
    """

    parts = urlparse(url)
    args = parse_qs(parts.query)
    # ParseResult is readonly, and actually is subclass of tuple
    parts = list(parts)
    args['bilin.ext'] = [ext_data]
    # update uri args
    parts[4] = urlencode(args, True)
    return urlunparse(parts)


def pop_url_macro(url):
    """
    Remove custom macro data in url args.
    Custom macro is like: bilin.ext=[4 random character]_u[USER_ID]t[TASK_ID],
    such as: bilin.ext=a1b2_u123t45678

    :return: tuple of (cleaned_url, macro_data)
    """
    parts = urlparse(url)
    args = parse_qs(parts.query)
    # no uri args
    if not args:
        return (url, None)
    else:
        # ParseResult is readonly, and actually is subclass of tuple
        parts = list(parts)
        ext = args.pop('bilin.ext', None)
        # update uri args
        parts[4] = urlencode(args, True)
        return (urlunparse(parts), ext and ext[0])


if __name__ == '__main__':
    url = 'http://www.google.com/?q=123&loc=us'
    new_url = set_url_macro(url, 'abcd_u123t3456')
    print(new_url)
    new_url, ext_data = pop_url_macro(new_url)
    print(new_url, ext_data)
