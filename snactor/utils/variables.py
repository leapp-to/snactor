def assign_to_variable_spec(data, spec, value):
    if not spec.startswith('@') or not spec.endswith('@'):
        raise ValueError("{} is not a reference".format(spec))
    parts = spec.strip('@').split('.')
    data.setdefault(parts[0], []).append({})
    gen = data[parts[0]][-1]
    for part in parts[1:-1]:
        gen[part] = {}
        gen = gen[part]
    gen[parts[-1]] = value
    return data[parts[0]][-1]


def resolve_variable_spec_items(data, spec):
    if isinstance(spec, (tuple, list)):
        return map(lambda item: resolve_variable_spec(data, item), spec)
    return resolve_variable_spec(data, spec),


def resolve_variable_spec(data, spec):
    if data and spec.startswith('@') and spec.endswith('@'):
        first = True
        for element in spec.strip('@').split('.'):
            data = data.get(element, None)
            if not data:
                break
            if first and isinstance(data, list):
                data = data[0]
                first = False
        if data is None:
            raise ValueError("unresolved reference: {}".format(spec.strip("@")))
        return data
    return spec
