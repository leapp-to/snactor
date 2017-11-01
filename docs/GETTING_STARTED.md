# Getting Started
snactor is a library written in Python to load, verify and execute an actor. An actor consists of a piece of code that can be executed and an yaml file that contains metadata about it, like: how it will be executed, messages it should receive as input, messages it will produce as output and so on. At this document we will describe how to write and execute a simple actor.


## Defining what the actor will do

On this example we will use a simple Bash Script that should be executed by our new actor but, snactor does support creating actors to execute code written in Python and other languages too.

Lets get a script to list all installed packages at a Fedora machine and place the result at a file named **packages.txt**. Lets call such script **list_packages.sh**:

```
$ ls
list_packages.sh

$ cat list_packages.sh
rpm -qa > packages.txt

$ bash list_packages.sh
$ ls
list_packages.sh  packages.txt

$ head -5 packages.txt
python3-pytest-pep8-1.0.6-9.fc26.noarch
pcre-8.41-1.fc26.x86_64
python2-fedora-0.9.0-6.fc26.noarch
libwpg-0.3.2-1.fc26.x86_64
tcl-8.6.6-2.fc26.x86_64
```


## Creating our new actor

By definition, all actor's files should be placed in a single directory. Let's name our new actor **list_packages**, create a directory structure and move our script inside of it:

```
└── actors
    └── list_packages
        └── list_packages.sh
```

As mentioned before, an actor needs to contain an yaml file defining, at least, how it should be executed by snactor. We will define which executor should be used, tell it to use Bash executable to run our script and, of course, point which script should be executed. Before closing it, we will add a description, that is not mandatory but always a good policy. Let's place all this info in a file named **_actor.yaml**:

```yaml
---
description: |
  An actor to list all installed packages
execute:
  executable: /bin/bash
  script-file: list_packages.sh
```

Our directory structure will look like this:

```
└── actors
    └── list_packages
        ├── _actor.yaml
        └── list_packages.sh
```


## Running our new actor

At this moment we are ready to execute our script as a snactor actor. To execute it you could either use **/usr/bin/snactor_runner** tool provided by snactor or write some Python code to load and run our new actor using the library. We will provide some sample runner script to show how to use snactor to get an actor executed:

```py
#!/usr/bin/env python
import os
from snactor.loader import load, get_actor


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    actors_dir = os.path.join(base_dir, 'actors')

    load(actors_dir)
    get_actor('list_packages').execute({})


if __name__ == '__main__':
    main()
```

First step is to point to snactor from which path to load the actors using *load()*. As soon as all actors are loaded we can get the desired one by the name using *get_actor()*. Finally we can call *execute()* to run the actor passing expected input messages as a parameter.

If we run this script we can verify that our actor was executed by checking the generated output file:

```
(...)
├── actors
│   └── list_packages
│       ├── _actor.yaml
│       └── list_packages.sh
└── execute.py

$ ./execute.py

(...)
├── actors
│   └── list_packages
│       ├── _actor.yaml
│       ├── list_packages.sh
│       └── packages.txt
└── execute.py

$ head -5 actors/list_packages/packages.txt
python3-pytest-pep8-1.0.6-9.fc26.noarch
pcre-8.41-1.fc26.x86_64
python2-fedora-0.9.0-6.fc26.noarch
libwpg-0.3.2-1.fc26.x86_64
tcl-8.6.6-2.fc26.x86_64
```


## Passing data to our actor ##

Now that we know how to write and execute an actor using snactor, let's see how to pass input data to it. We will change our actor to receive a string as input and use it to filter the generated list of packages. First step, we need to update our actor's yaml to describe a name and type of input data:

```yaml
---
inputs:
  - name: filter
    type:
      name: PackageFilter
description: |
  An actor to list all installed packages
execute:
  executable: /bin/bash
  script-file: list_packages.sh
```

We should list under *inputs* a name identifier and a type for each input data that our script will receive.
Here we are defining a **filter** input of type **PackageFilter**.
With snactor all data used as input or output for an actor is formatted as JSON and the used schema is defined, using JSL, by the provided type.
That way we need to tell snactor how **PackageFilter** type looks like.
We will save such definition in a Python file named **packagefilter.py**:

```py
from jsl import Document
from jsl.fields import StringField
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class PackageFilter(Document):
    value = StringField()
```

and save it under a directory named **schemas**:

```
├── actors
│   └── list_packages
│       ├── _actor.yaml
│       └── list_packages.sh
├── execute.py
└── schemas
    └── packagefilter.py
```

All these names are arbitrary and you can change them as you wish.

With input data defined we need to change our script to receive such input and filter the list of package with it:

```shell
input=""
while read line; do
  input+=${line}
done < "${1:-/dev/stdin}"

filter=$(echo ${input} | python -c "\
import json, sys
obj=json.load(sys.stdin)
print(obj[\"filter\"][0][\"value\"])")

rpm -qa | grep ${filter} > packages.txt
```

Finally, to be able to test it, we should change our **executor.py** script to pass some filter string to our actor:

```py
#!/usr/bin/env python
import os
from snactor.loader import load, load_schemas, validate_actor_types, get_actor


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    actors_dir = os.path.join(base_dir, 'actors')
    schemas_dir = os.path.join(base_dir, 'schemas')

    data = {'filter': [{'value': 'python'}]}

    load(actors_dir)
    load_schemas(schemas_dir)
    validate_actor_types()

    get_actor('list_packages').execute(data)


if __name__ == '__main__':
    main()
```

We need to tell snactor from where to load type schemas using *load_schemas()*. Also, we are calling *validate_actor_types()* to let snactor verify if all used types are well defined. Again, this is not mandatory. Look that instead of providing empty data to *execute()*, now we are calling it passing **"python"** as the filter string, respecting the defined JSON schema. After running this, we can verify that **packages.txt** has only packages that contain **"python"** in the name.

```
$ head -5 actors/list_packages/packages.txt
python3-pytest-pep8-1.0.6-9.fc26.noarch
python2-fedora-0.9.0-6.fc26.noarch
python3-dnf-plugins-core-2.1.3-1.fc26.noarch
python2-SecretStorage-2.3.1-4.fc26.noarch
python2-iniparse-0.4-24.fc26.noarch
```


## Retrieving data from our actor ##

Right now, we are saving the generated package list to a text file. That is fine, but what if we want to pass such a list for another actor in the same way we passed filter string to this one? To support that we can define and actor's outputs in the same way we defined the inputs. So, let's change our actor to return the package list as output data.

As we did before, first step is update actor's yaml to describe output. We will add an output named **packages** of type **PackagesList**:

```yaml
---
inputs:
  - name: filter
    type:
      name: PackageFilter
outputs:
  - name: packages
    type:
      name: PackagesList
description: |
  An actor to list all installed packages
execute:
  executable: /bin/bash
  script-file: list_packages.sh
```

Next, we should tell snactor what **PackagesList** is.
Create **packageslist.py**:

```py
from jsl import ArrayField, Document
from jsl.fields import StringField
from snactor.registry.schemas import registered_schema


@registered_schema('1.0')
class PackagesList(Document):
    entries = ArrayField(StringField())
```

and put it inside the **schemas** directory:

```
├── actors
│   └── list_packages
│       ├── _actor.yaml
│       └── list_packages.sh
├── execute.py
└── schemas
    ├── packagefilter.py
    └── packageslist.py
```

Now, we have to change our bash script to output data with the specified format:

```shell
input=""
while read line; do
  input+=${line}
done < "${1:-/dev/stdin}"

filter=$(echo ${input} | python -c "\
import json, sys
obj=json.load(sys.stdin)
print(obj[\"filter\"][0][\"value\"])")

entries=$(rpm -qa | grep ${filter} | awk '{ print "\""$0"\""}' | tr '\n' ',' | sed 's/,$//')

echo -e "{\"packages\": [{\"entries\": [${entries}]}]}"
```

If we change our **executor.py** script to print the returned data from our actor, we can verify that now the packages list is being returned as output data:

```py
#!/usr/bin/env python
import os
from pprint import pprint
from snactor.loader import load, load_schemas, validate_actor_types, get_actor


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    actors_dir = os.path.join(base_dir, 'actors')
    schemas_dir = os.path.join(base_dir, 'schemas')

    data = {'filter': [{'value': 'python'}]}

    load(actors_dir)
    load_schemas(schemas_dir)
    validate_actor_types()

    get_actor('list_packages').execute(data)

    pprint(data['packages'])


if __name__ == '__main__':
    main()
```

Note that the same data object used to pass input data is updated to contain output data.

```
$ ./execute.py
{u'entries': [u'python3-pytest-pep8-1.0.6-9.fc26.noarch',
              u'python2-fedora-0.9.0-6.fc26.noarch',
              u'python3-dnf-plugins-core-2.1.3-1.fc26.noarch',
              u'python2-SecretStorage-2.3.1-4.fc26.noarch',
              (...)
              u'python2-bcrypt-3.1.3-1.fc26.x86_64']}
```
