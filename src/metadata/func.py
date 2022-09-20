import logging


def raise_exception(exception: Exception):
    logging.warning(exception)


def make_unique_string(init_str: str, list_str: list[str]) -> str:
    s = init_str
    i = 0
    while s in list_str:
        i += 1
        s = f"{init_str} {i}"
    return s
