"""
String helper:
cleans the string, de-duplicates List, Joins address parts in proper format
"""
import unicodedata
import re


def remove_white_spaces(input_string):
    """
    Removes continuous spaces in the input string
    :param input_string:
    """
    return re.sub(r'\s+', ' ', input_string).strip()


def remove_unicode_characters(input_string):
    """ strips unicode characters in the string
    :param input_string:
    """
    return unicodedata.normalize('NFKD', input_string).encode('ascii', 'ignore')


def process_string(input_string):
    """ aggregation of remove_white_spaces and remove_unicode_characters to clean the string
    :param input_string:
    """
    return remove_white_spaces(remove_unicode_characters(input_string))


def deduplicate_list(input_list):
    """
    Filters duplicate entry from list while preserving original order of list
    :param input_list:
    :return:
    """
    seen = set()
    seen_add = seen.add
    return [x for x in input_list if not (x in seen or seen_add(x))]


def join_address_elements(address_parts):
    """
    joins address parts in english format and remove empty address parts
    :param address_parts:
    """
    return ', '.join(a.strip() for a in address_parts if re.search(r'\S', a))
