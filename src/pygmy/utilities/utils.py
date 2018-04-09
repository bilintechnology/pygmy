import re
from pygmy.config import config


def make_url_from_id(_id, url_type):
    """Builds an url from the object passed."""
    base_url = config.webservice_url
    url_type_mapping = dict(
        user=base_url + '/api/user/{}',
        link=base_url + '/api/link/{}',
        links_list=base_url + '/api/user/{}/links'
    )
    return url_type_mapping.get(url_type).format(_id)


__MACRO_REGEX = re.compile(r'[0-9a-zA-Z]{4}_u(\d+)t(\d+)')


def extract_macro(ext_data):
    """
    Extract user id and task id from macro value.
    "abcd_u123t3456" return (123, 3456)

    :return: tuple of (user_id, task_id)
    """
    m = __MACRO_REGEX.match(ext_data)
    if not m:
        return (None, None)
    else:
        return m.groups()
