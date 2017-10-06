# snactor
Python Actor execution library

## Actor Definitions

### Actor Definition Format

```yaml
---
inputs:
  - name: input_channel_name
    type:
        name: schema_name_reference
        version: 1.0
outputs:
  name: output_channel_name
  type:
    name: schema_name_reference
    version: 1.0
description: |
  Text field to describe what this actor is doing and a potential place
  for documenting the inputs and outputs
```

In case this is executing something directly this section is required:
```
execute:
    type: default
    executable: path-to-executable

    script-file: relative-path-to-a-script-in-the-actor-directory
    # path to a file with the special property of being the
    # first argument to the executable specified as executable

    arguments:
        - ...
```

If this definition just defines a group of actors to be executed,
the group field with a list of actor names has to be specified
```
group:
- actor-name
- another-actor-name
```
