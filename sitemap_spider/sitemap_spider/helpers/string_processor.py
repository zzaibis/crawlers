def deduplicate_list(input_list):
    """
    Filters duplicate entry from list while preserving original order of list
    :param input_list:
    :return:
    """
    seen = set()
    seen_add = seen.add
    return [x for x in input_list if not (x in seen or seen_add(x))]

