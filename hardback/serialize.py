import attr


def unserialize(data, item):
    """Unserialize from JSON-like data to a dataclass (dicts, strings, etc)"""
    try:
        fields = attr.fields_dict(item.__class__)
    except:
        try:
            return type(item)(data)
        except:
            return data

    unknown = set(data) - set(fields)
    if unknown:
        raise ValueError('Do not understand fields:', *unknown)

    for k, v in data.items():
        subitem = getattr(item, k)
        setattr(item, k, unserialize(v, subitem))

    return item


def serialize(item):
    """Serialize from a dataclass to JSON-like data"""
    return attr.asdict(item)
