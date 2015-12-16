#!/usr/bin/env python
from __future__ import print_function
from ptrace import PtraceError
from ptrace.binding import func
from ptrace.debugger import (
    PtraceDebugger, Application,
    ProcessExit, ProcessSignal, NewProcessEvent, ProcessExecution)
from ptrace.func_call import FunctionCallOptions
from sys import stdout, stderr, exit
from optparse import OptionParser
from logging import getLogger, error
from ptrace.error import PTRACE_ERRORS, writeError
import sys


class SyscallTracer(Application):

    def __init__(self):
        Application.__init__(self)

        # Parse self.options
        self.parseOptions()

        # Setup output (log)
        self.setupLog()

    def setupLog(self):
        if self.options.output:
            fd = open(self.options.output, 'w')
            self._output = fd
        else:
            fd = stderr
            self._output = None
        self._setupLog(fd)

    def parseOptions(self):
        parser = OptionParser(usage="%prog pid")
        parser.add_option(
            "--no-fork", "-n", help="Don't trace forks",
            action="store_false", dest="fork", default=True)

        if len(sys.argv) == 1:
            parser.print_help()
            exit(1)

        self.options, self.program = parser.parse_args()
        defaults = (
            ('pid', int(sys.argv[1])),
            ('trace_exec', False),
            ('enter', False),
            ('profiler', False),
            ('type', False),
            ('name', False),
            ('string_length', 99999999),
            ('array_count', 20),
            ('raw_socketcall', False),
            ('output', ''),
            ('ignore_regex', ''),
            ('address', False),
            ('syscalls', None),
            ('socket', False),
            ('filename', False),
            ('show_pid', False),
            ('list_syscalls', False),
            ('show_ip', False),
            ('debug', False),
            ('verbose', False),
            ('quiet', False),
        )
        for option, value in defaults:
            setattr(self.options, option, value)

        self.only = set()
        self.ignore_regex = None

        if self.options.fork:
            self.options.show_pid = True

        self.processOptions()

    def ignoreSyscall(self, syscall):
        name = syscall.name
        if self.only and (name not in self.only):
            return True
        if self.ignore_regex and self.ignore_regex.match(name):
            return True
        return False

    def displaySyscall(self, syscall):
        if syscall.name == 'write':
            fd = syscall.arguments[0].value
            if fd < 3:
                text = syscall.arguments[1].getText()[1:-1]
                stdout.write(text.decode('string_escape'))
                stdout.flush()

    def syscallTrace(self, process):
        # First query to break at next syscall
        self.prepareProcess(process)

        while True:
            # No more process? Exit
            if not self.debugger:
                break

            # Wait until next syscall enter
            try:
                event = self.debugger.waitSyscall()
                process = event.process
            except ProcessExit as event:
                self.processExited(event)
                continue
            except ProcessSignal as event:
                # event.display()
                process.syscall(event.signum)
                continue
            except NewProcessEvent as event:
                self.newProcess(event)
                continue
            except ProcessExecution as event:
                self.processExecution(event)
                continue

            # Process syscall enter or exit
            self.syscall(process)

    def syscall(self, process):
        state = process.syscall_state
        syscall = state.event(self.syscall_options)
        if syscall and (syscall.result is not None or self.options.enter):
            self.displaySyscall(syscall)

        # Break at next syscall
        process.syscall()

    def processExited(self, event):
        # Display syscall which has not exited
        state = event.process.syscall_state
        if (state.next_event == "exit") \
                and (not self.options.enter) \
                and state.syscall:
            self.displaySyscall(state.syscall)

    def prepareProcess(self, process):
        process.syscall()
        process.syscall_state.ignore_callback = self.ignoreSyscall

    def newProcess(self, event):
        process = event.process
        self.prepareProcess(process)
        process.parent.syscall()

    def processExecution(self, event):
        process = event.process
        process.syscall()

    def runDebugger(self):
        # Create debugger and traced process
        self.setupDebugger()
        process = self.createProcess()
        if not process:
            return

        self.syscall_options = FunctionCallOptions(
            write_types=self.options.type,
            write_argname=self.options.name,
            string_max_length=self.options.string_length,
            replace_socketcall=not self.options.raw_socketcall,
            write_address=self.options.address,
            max_array_count=self.options.array_count,
        )
        self.syscall_options.instr_pointer = self.options.show_ip

        self.syscallTrace(process)

    def main(self):
        self._main()
        if self._output is not None:
            self._output.close()

    def _main(self):
        self.debugger = PtraceDebugger()
        try:
            self.runDebugger()
        except ProcessExit as event:
            self.processExited(event)
        except PtraceError as err:
            error("ptrace() error: %s" % err)
        except KeyboardInterrupt:
            error("Interrupted.")
        except PTRACE_ERRORS as err:
            writeError(getLogger(), err, "Debugger error")
        self.debugger.quit()

    def createChild(self, program):
        pid = Application.createChild(self, program)
        error("execve(%s, %s, [/* 40 vars */]) = %s" % (
            program[0], program, pid))
        return pid


def main():
    SyscallTracer().main()


if __name__ == "__main__":
    main()
