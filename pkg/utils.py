def deep_update(original: dict, update: dict):
    """
    original = {'a': 'x', 'b': {'ba': 'x', 'bc': 'x'}}
    update = {'b': {'ba': 'y'}}

    deep_update(original, update)

    print(original) # {'a': 'x', 'b': {'ba': 'y', 'bc': 'x'}}
    """
    for key, value in update.items():
        if (
            isinstance(value, dict)
            and key in original
            and isinstance(original[key], dict)
        ):
            deep_update(original[key], value)
        else:
            original[key] = value
    return original
