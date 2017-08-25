---
description: |
  This actor should not be loaded because it have both an extends and a executor
tags:
  - extends_executor_actor
outputs:
  - name: foo
    type: Foo
extends:
  name: some_packages
executor:
  type: default
  executable: /bin/bash
  arguments:
    - "-c"
    - "echo {\\\"foo\\\": \\\"bar\\\"}"
