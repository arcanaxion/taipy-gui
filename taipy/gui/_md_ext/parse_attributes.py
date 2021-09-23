def parse_attributes(input: str):
    # TODO: very simplistic version of what this should do.
    # so far, only a list or comma-separated key-value pairs are handled
    if not input:
        return None
    attributes = {}
    for attribute in input.split(","):
        pair = attribute.split("=")
        if len(pair) > 2:
            raise ValueError(f"Invalid attribute syntax: '{attribute}'")
        attributes[pair[0].strip()] = str(True) if len(pair) == 1 else pair[1].strip()
    return attributes