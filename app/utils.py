def omit(_dict, keys):
    return {key: _dict[key] for key in _dict if key not in keys}
