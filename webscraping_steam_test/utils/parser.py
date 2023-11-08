from selectolax.parser import HTMLParser, Node

def parse_raw_attributes(node: Node, selectors: list):
    parsed = {

    }

    for s in selectors:
        match = s.get('match')
        name = s.get('name')
        selector = s.get('selector')
        type = s.get('type')

        if match == 'all':
            matched = node.css(selector)

            if type == 'text':
                if (matched is None):
                    parsed[name] = "N/A"
                else:
                    parsed[name] = [m.text() for m in matched]
            elif type == 'node':
                parsed[name] = matched

        elif match == 'first':
            matched = node.css_first(selector)

            if type == 'text':
                if(matched is None):
                    parsed[name] = "N/A"
                else:
                    parsed[name] = matched.text()
            elif type == 'node':
                parsed[name] = matched

    return parsed