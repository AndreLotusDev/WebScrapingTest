from datetime import datetime

from selectolax.parser import Node

def get_attrs_from_node(node: Node, attr: str):
    if node:
        return node.attributes.get(attr)

    return None

def get_first_n(input_list: list, n: int):
    if input_list:
        value_to_return = input_list[:n]
        return value_to_return

    return None

def reformat_date(date: str, old_format: str, new_format: str):
    if date:
        return datetime.strptime(date, old_format).strftime(new_format)

    return None

def format_and_transform(attrs: dict):
    transforms = {
        "thumbnail": lambda n: get_attrs_from_node(n, "src"),
        "tags": lambda input_list: get_first_n(input_list, 5),
        "release_date": lambda date: reformat_date(date, "%b %d, %Y", "%Y-%m-%d"),
    }

    for k, v in transforms.items():
        if k in attrs:
            attrs[k] = v(attrs[k])


    return attrs