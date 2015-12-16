# ispy

`ispy` is a python tool for monitoring the output of terminals and processes.

## Installation

    pip install ispy

## Usage

    # ispy <pid_to_watch>

## Demo

`ispy` watching a bash session that lists some files and opens `vim`:

![ispy demo](https://github.com/dellis23/ispy/blob/master/img/ispydemo.gif)

The same thing, using `strace`:

![strace watching writes demo](https://github.com/dellis23/ispy/blob/master/img/ispydemo-strace.gif)

## Use Cases

 * Watching someone else's terminal
 * Watching the output of a backgrounded process

## Notes

### Take care in production

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