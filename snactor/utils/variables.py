def assign_to_variable_spec(data, spec, value):
    if not spec.startswith('@') or not spec.endswith('@'):
        raise ValueError("{} is not a reference".format(spec))
    parts = spec.strip('@').split('.')
    data[parts[0]] = {}
    gen = data[parts[0]]
    for part in parts[1:-1]:
        gen[part] = {}
        gen = gen[part]
    gen[parts[-1]] = value
    return data[parts[0]]


def resolve_variable_spec(data, spec):
    if data and spec.startswith('@') and spec.endswith('@'):
        for element in spec.strip('@').split('.'):
            data = data.get(element, None)
            if not data:
                break
        if not data:
            raise ValueError("unresolved reference")
        return data
    return spec
