# snactor
Python Actor execution library - POC at this moment


## Actor Definitions

There are two kinds of definitions:

1. Actor Definition
2. Actor Extension Definition

Extension definitions allow to specialize other actor definitions
and build new actors trough this. Extensions also allow for connecting
two unrelated previously unrelated names.

### Actor Definition Format

```yaml
---
inputs:
  - name: input_channel_name
    type: schema_name_reference
outputs:
  name: output_channel_name
  type: schema_name_reference
description: |
  Text field to describe what this actor is doing and a potential place
  for documenting the inputs and outputs
executor:
    type: registered-name-of-executor
    ... executor specific fields
```

### Actor Extension Definition Format

```yaml
---
inputs:
  - name: input_channel_name
    type: schema_name_reference
outputs:
  name: output_channel_name
  type: schema_name_reference
description: |
  Text field to describe what this actor is doing and a potential place
  for documenting the inputs and outputs
extends:
  name: actor_name_to_extend
  inputs:
    - name: input_channel_name_of_the_extended_actor
      value: value_to_pass
    - name: input_channel_name_of_the_extended_actor2
      source: '@input_channel_name.to.pass.through.to.the.actor.in.reference.notation@'
  outputs:
    - name: output_channel_name
      source: '@output_channel_name.to.return.in.reference.notation@'

```


## Provided executors
### DefaultExecutor
```yaml
---
executor:
    type: default
    executable: path-to-executable
    arguments:
        - ...
```


### PayloadExecutor
```yaml
---
executor:
    type: default
    executable: path-to-executable
    arguments:
        - ...
    # instead of payload script-file can be used to specify a script
    # which will be passed as a first parameter to the executable
    # script-file: path/to/script
```

### BashExecutor
```yaml
---
executor:
    type: bash
    arguments:
        - ...
    payload: |
        #!/bin/bash
        echo '{"message": {"value": "This is a bash executor script"}}'
    # instead of payload script-file can be used to specify a script
    # script-file: path/to/script
```

The BashExecutor has some speciality called output-processor that can process
the output from stdout of the script and transform it to specified format.
Right now there is only the string-list processor that splits lines from stdout and
converts it to a string list as specified in the target field.
```yaml
    output-processor:
        - type: string-list
          target: '@output_name.field_name@'
```

### PythonExecutor
```yaml
---
executor:
    type: default
    executable: path-to-executable
    arguments:
        - ...
    payload: |
        import json
        print json.dumps({"message": {"value": "This is a python executor script"}})
    # instead of payload script-file can be used to specify a script
    # script-file: path/to/script
```

### GroupExecutor
```yaml
---
executor:
    type: default
    actors:
        - actor-name
        - another-actor-name
```

