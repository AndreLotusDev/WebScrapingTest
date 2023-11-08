from selectolax.parser import Node

def get_attrs_from_node(node: Node, attr: str):
    if node:
        return node.attributes.get(attr)

    return None

def format_and_transform(attrs: dict):
    transforms = {
        "thumbnail": lambda n: get_attrs_from_node(n, "src")
    }

    for k, v in transforms.items():
        if k in attrs:
            attrs[k] = v(attrs[k])


    return attrs