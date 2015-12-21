# ispy

`ispy` is a python tool for monitoring the output of terminals and processes.

## Demo

`ispy` watching a `bash` session that lists some files and opens `vim`:

![ispy demo](https://github.com/dellis23/ispy/blob/master/img/ispydemo.gif)

The same thing, using `strace`:

![strace watching writes demo](https://github.com/dellis23/ispy/blob/master/img/ispydemo-strace.gif)

## Installation

    pip install ispy
    
Alternatively, if you aren't a Python person or don't want to install it
(since it must be run as root), you can download a fully packaged 
[`pex`](https://pex.readthedocs.org/en/latest/) file and run without 
installing:

    wget https://github.com/dellis23/ispy/blob/master/bin/pex/ispy.pex?raw=true -O ispy; chmod +x ispy

## Usage

    # ispy <pid_to_watch>

## Use Cases

 * Watching someone else's terminal
 * Watching the output of a backgrounded process

## Notes

### **Not** intended for production!

It's probably buggy.

This was mainly an exercise in learning about `ptrace` for myself.  I
haven't done anything more than smoke testing on a couple of 
operating systems.

This uses the same system call as `strace` (`ptrace`), which is heavy-handed
and has a performance impact.  It is not recommended to use in production or
against mission-critical applications.  It's also written in Python, so it's even slower.

### Supported OSs

This has been tested as working on:

 * Ubuntu
 * CentOS

This has been tested as **not** working on:

 * OSX

## Thanks

Thanks to the creator and maintainers of [python-ptrace](https://bitbucket.org/haypo/python-ptrace/); this project depends on it.