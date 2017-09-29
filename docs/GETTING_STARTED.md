# Getting Started
snactor is a library written in Python to load, verify and execute an actor. An actor consists of a piece of code that can be executed and an yaml file that contains metadata about it. For example, how it will be executed, messages it should receive as input, messages it will produce as output and so on. At this document we will describe how to write and executea sample actor.


## Defining what the Actor will do

On this example we will use a simple Bash Script that should be executed by our new actor but snactor does support creating actors to execute code written in Python and other languages too.

Lets get a script to list all installed packages at a Fedora Machine and save the result at a file name packages.txt.

```
rpm -qa > packages.txt
```
