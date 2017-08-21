def assign_to_variable_spec(data, spec, value):
    if not spec.startswith('@') or not spec.endswith('@'):
        raise ValueError("{} is not a reference".format(spec))
    parts = spec.strip('@').split('.')
    obj = resolve_variable_spec(data, '@{}@'.format('.'.join(parts[:-1])))
    if not obj or parts[-1] not in obj:
        raise ValueError("Unresolved reference")
    else:
        obj[parts[-1]] = value
    return data


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
