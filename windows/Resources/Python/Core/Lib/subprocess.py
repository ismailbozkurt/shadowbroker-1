# uncompyle6 version 2.9.10
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.0b2 (default, Oct 11 2016, 05:27:10) 
# [GCC 6.2.0 20161005]
# Embedded file name: subprocess.py
r"""subprocess - Subprocesses with accessible I/O streams

This module allows you to spawn processes, connect to their
input/output/error pipes, and obtain their return codes.  This module
intends to replace several other, older modules and functions, like:

os.system
os.spawn*
os.popen*
popen2.*
commands.*

Information about how the subprocess module can be used to replace these
modules and functions can be found below.



Using the subprocess module
===========================
This module defines one class called Popen:

class Popen(args, bufsize=0, executable=None,
            stdin=None, stdout=None, stderr=None,
            preexec_fn=None, close_fds=False, shell=False,
            cwd=None, env=None, universal_newlines=False,
            startupinfo=None, creationflags=0):


Arguments are:

args should be a string, or a sequence of program arguments.  The
program to execute is normally the first item in the args sequence or
string, but can be explicitly set by using the executable argument.

On UNIX, with shell=False (default): In this case, the Popen class
uses os.execvp() to execute the child program.  args should normally
be a sequence.  A string will be treated as a sequence with the string
as the only item (the program to execute).

On UNIX, with shell=True: If args is a string, it specifies the
command string to execute through the shell.  If args is a sequence,
the first item specifies the command string, and any additional items
will be treated as additional shell arguments.

On Windows: the Popen class uses CreateProcess() to execute the child
program, which operates on strings.  If args is a sequence, it will be
converted to a string using the list2cmdline method.  Please note that
not all MS Windows applications interpret the command line the same
way: The list2cmdline is designed for applications using the same
rules as the MS C runtime.

bufsize, if given, has the same meaning as the corresponding argument
to the built-in open() function: 0 means unbuffered, 1 means line
buffered, any other positive value means use a buffer of
(approximately) that size.  A negative bufsize means to use the system
default, which usually means fully buffered.  The default value for
bufsize is 0 (unbuffered).

stdin, stdout and stderr specify the executed programs' standard
input, standard output and standard error file handles, respectively.
Valid values are PIPE, an existing file descriptor (a positive
integer), an existing file object, and None.  PIPE indicates that a
new pipe to the child should be created.  With None, no redirection
will occur; the child's file handles will be inherited from the
parent.  Additionally, stderr can be STDOUT, which indicates that the
stderr data from the applications should be captured into the same
file handle as for stdout.

If preexec_fn is set to a callable object, this object will be called
in the child process just before the child is executed.

If close_fds is true, all file descriptors except 0, 1 and 2 will be
closed before the child process is executed.

if shell is true, the specified command will be executed through the
shell.

If cwd is not None, the current directory will be changed to cwd
before the child is executed.

If env is not None, it defines the environment variables for the new
process.

If universal_newlines is true, the file objects stdout and stderr are
opened as a text files, but lines may be terminated by any of '\n',
the Unix end-of-line convention, '\r', the Macintosh convention or
'\r\n', the Windows convention.  All of these external representations
are seen as '\n' by the Python program.  Note: This feature is only
available if Python is built with universal newline support (the
default).  Also, the newlines attribute of the file objects stdout,
stdin and stderr are not updated by the communicate() method.

The startupinfo and creationflags, if given, will be passed to the
underlying CreateProcess() function.  They can specify things such as
appearance of the main window and priority for the new process.
(Windows only)


This module also defines some shortcut functions:

call(*popenargs, **kwargs):
    Run command with arguments.  Wait for command to complete, then
    return the returncode attribute.

    The arguments are the same as for the Popen constructor.  Example:

    retcode = call(["ls", "-l"])

check_call(*popenargs, **kwargs):
    Run command with arguments.  Wait for command to complete.  If the
    exit code was zero then return, otherwise raise
    CalledProcessError.  The CalledProcessError object will have the
    return code in the returncode attribute.

    The arguments are the same as for the Popen constructor.  Example:

    check_call(["ls", "-l"])

check_output(*popenargs, **kwargs):
    Run command with arguments and return its output as a byte string.

    If the exit code was non-zero it raises a CalledProcessError.  The
    CalledProcessError object will have the return code in the returncode
    attribute and output in the output attribute.

    The arguments are the same as for the Popen constructor.  Example:

    output = check_output(["ls", "-l", "/dev/null"])


Exceptions
----------
Exceptions raised in the child process, before the new program has
started to execute, will be re-raised in the parent.  Additionally,
the exception object will have one extra attribute called
'child_traceback', which is a string containing traceback information
from the childs point of view.

The most common exception raised is OSError.  This occurs, for
example, when trying to execute a non-existent file.  Applications
should prepare for OSErrors.

A ValueError will be raised if Popen is called with invalid arguments.

check_call() and check_output() will raise CalledProcessError, if the
called process returns a non-zero return code.


Security
--------
Unlike some other popen functions, this implementation will never call
/bin/sh implicitly.  This means that all characters, including shell
metacharacters, can safely be passed to child processes.


Popen objects
=============
Instances of the Popen class have the following methods:

poll()
    Check if child process has terminated.  Returns returncode
    attribute.

wait()
    Wait for child process to terminate.  Returns returncode attribute.

communicate(input=None)
    Interact with process: Send data to stdin.  Read data from stdout
    and stderr, until end-of-file is reached.  Wait for process to
    terminate.  The optional input argument should be a string to be
    sent to the child process, or None, if no data should be sent to
    the child.

    communicate() returns a tuple (stdout, stderr).

    Note: The data read is buffered in memory, so do not use this
    method if the data size is large or unlimited.

The following attributes are also available:

stdin
    If the stdin argument is PIPE, this attribute is a file object
    that provides input to the child process.  Otherwise, it is None.

stdout
    If the stdout argument is PIPE, this attribute is a file object
    that provides output from the child process.  Otherwise, it is
    None.

stderr
    If the stderr argument is PIPE, this attribute is file object that
    provides error output from the child process.  Otherwise, it is
    None.

pid
    The process ID of the child process.

returncode
    The child return code.  A None value indicates that the process
    hasn't terminated yet.  A negative value -N indicates that the
    child was terminated by signal N (UNIX only).


Replacing older functions with the subprocess module
====================================================
In this section, "a ==> b" means that b can be used as a replacement
for a.

Note: All functions in this section fail (more or less) silently if
the executed program cannot be found; this module raises an OSError
exception.

In the following examples, we assume that the subprocess module is
imported with "from subprocess import *".


Replacing /bin/sh shell backquote
---------------------------------
output=`mycmd myarg`
==>
output = Popen(["mycmd", "myarg"], stdout=PIPE).communicate()[0]


Replacing shell pipe line
-------------------------
output=`dmesg | grep hda`
==>
p1 = Popen(["dmesg"], stdout=PIPE)
p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
output = p2.communicate()[0]


Replacing os.system()
---------------------
sts = os.system("mycmd" + " myarg")
==>
p = Popen("mycmd" + " myarg", shell=True)
pid, sts = os.waitpid(p.pid, 0)

Note:

* Calling the program through the shell is usually not required.

* It's easier to look at the returncode attribute than the
  exitstatus.

A more real-world example would look like this:

try:
    retcode = call("mycmd" + " myarg", shell=True)
    if retcode < 0:
        print >>sys.stderr, "Child was terminated by signal", -retcode
    else:
        print >>sys.stderr, "Child returned", retcode
except OSError, e:
    print >>sys.stderr, "Execution failed:", e


Replacing os.spawn*
-------------------
P_NOWAIT example:

pid = os.spawnlp(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg")
==>
pid = Popen(["/bin/mycmd", "myarg"]).pid


P_WAIT example:

retcode = os.spawnlp(os.P_WAIT, "/bin/mycmd", "mycmd", "myarg")
==>
retcode = call(["/bin/mycmd", "myarg"])


Vector example:

os.spawnvp(os.P_NOWAIT, path, args)
==>
Popen([path] + args[1:])


Environment example:

os.spawnlpe(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg", env)
==>
Popen(["/bin/mycmd", "myarg"], env={"PATH": "/usr/bin"})


Replacing os.popen*
-------------------
pipe = os.popen("cmd", mode='r', bufsize)
==>
pipe = Popen("cmd", shell=True, bufsize=bufsize, stdout=PIPE).stdout

pipe = os.popen("cmd", mode='w', bufsize)
==>
pipe = Popen("cmd", shell=True, bufsize=bufsize, stdin=PIPE).stdin


(child_stdin, child_stdout) = os.popen2("cmd", mode, bufsize)
==>
p = Popen("cmd", shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, close_fds=True)
(child_stdin, child_stdout) = (p.stdin, p.stdout)


(child_stdin,
 child_stdout,
 child_stderr) = os.popen3("cmd", mode, bufsize)
==>
p = Popen("cmd", shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
(child_stdin,
 child_stdout,
 child_stderr) = (p.stdin, p.stdout, p.stderr)


(child_stdin, child_stdout_and_stderr) = os.popen4("cmd", mode,
                                                   bufsize)
==>
p = Popen("cmd", shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
(child_stdin, child_stdout_and_stderr) = (p.stdin, p.stdout)

On Unix, os.popen2, os.popen3 and os.popen4 also accept a sequence as
the command to execute, in which case arguments will be passed
directly to the program without shell intervention.  This usage can be
replaced as follows:

(child_stdin, child_stdout) = os.popen2(["/bin/ls", "-l"], mode,
                                        bufsize)
==>
p = Popen(["/bin/ls", "-l"], bufsize=bufsize, stdin=PIPE, stdout=PIPE)
(child_stdin, child_stdout) = (p.stdin, p.stdout)

Return code handling translates as follows:

pipe = os.popen("cmd", 'w')
...
rc = pipe.close()
if rc is not None and rc % 256:
    print "There were some errors"
==>
process = Popen("cmd", 'w', shell=True, stdin=PIPE)
...
process.stdin.close()
if process.wait() != 0:
    print "There were some errors"


Replacing popen2.*
------------------
(child_stdout, child_stdin) = popen2.popen2("somestring", bufsize, mode)
==>
p = Popen(["somestring"], shell=True, bufsize=bufsize
          stdin=PIPE, stdout=PIPE, close_fds=True)
(child_stdout, child_stdin) = (p.stdout, p.stdin)

On Unix, popen2 also accepts a sequence as the command to execute, in
which case arguments will be passed directly to the program without
shell intervention.  This usage can be replaced as follows:

(child_stdout, child_stdin) = popen2.popen2(["mycmd", "myarg"], bufsize,
                                            mode)
==>
p = Popen(["mycmd", "myarg"], bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, close_fds=True)
(child_stdout, child_stdin) = (p.stdout, p.stdin)

The popen2.Popen3 and popen2.Popen4 basically works as subprocess.Popen,
except that:

* subprocess.Popen raises an exception if the execution fails
* the capturestderr argument is replaced with the stderr argument.
* stdin=PIPE and stdout=PIPE must be specified.
* popen2 closes all filedescriptors by default, but you have to specify
  close_fds=True with subprocess.Popen.
"""
import sys
mswindows = sys.platform == 'win32'
import os
import types
import traceback
import gc
import signal
import errno

class CalledProcessError(Exception):
    """This exception is raised when a process run by check_call() or
    check_output() returns a non-zero exit status.
    The exit status will be stored in the returncode attribute;
    check_output() will also store the output in the output attribute.
    """

    def __init__(self, returncode, cmd, output=None):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output

    def __str__(self):
        return "Command '%s' returned non-zero exit status %d" % (self.cmd, self.returncode)


if mswindows:
    import threading
    import msvcrt
    import _subprocess

    class STARTUPINFO():
        dwFlags = 0
        hStdInput = None
        hStdOutput = None
        hStdError = None
        wShowWindow = 0


    class pywintypes():
        error = IOError


else:
    import select
    _has_poll = hasattr(select, 'poll')
    import fcntl
    import pickle
    _PIPE_BUF = getattr(select, 'PIPE_BUF', 512)
__all__ = [
 'Popen', 'PIPE', 'STDOUT', 'call', 'check_call',
 'check_output', 'CalledProcessError']
if mswindows:
    from _subprocess import CREATE_NEW_CONSOLE, CREATE_NEW_PROCESS_GROUP, STD_INPUT_HANDLE, STD_OUTPUT_HANDLE, STD_ERROR_HANDLE, SW_HIDE, STARTF_USESTDHANDLES, STARTF_USESHOWWINDOW
    __all__.extend(['CREATE_NEW_CONSOLE', 'CREATE_NEW_PROCESS_GROUP',
     'STD_INPUT_HANDLE', 'STD_OUTPUT_HANDLE',
     'STD_ERROR_HANDLE', 'SW_HIDE',
     'STARTF_USESTDHANDLES', 'STARTF_USESHOWWINDOW'])
try:
    MAXFD = os.sysconf('SC_OPEN_MAX')
except:
    MAXFD = 256

_active = []

def _cleanup():
    for inst in _active[:]:
        res = inst._internal_poll(_deadstate=sys.maxint)
        if res is not None and res >= 0:
            try:
                _active.remove(inst)
            except ValueError:
                pass

    return


PIPE = -1
STDOUT = -2

def _eintr_retry_call(func, *args):
    while True:
        try:
            return func(*args)
        except OSError as e:
            if e.errno == errno.EINTR:
                continue
            raise


def call(*popenargs, **kwargs):
    """Run command with arguments.  Wait for command to complete, then
    return the returncode attribute.
    
    The arguments are the same as for the Popen constructor.  Example:
    
    retcode = call(["ls", "-l"])
    """
    return Popen(*popenargs, **kwargs).wait()


def check_call(*popenargs, **kwargs):
    """Run command with arguments.  Wait for command to complete.  If
    the exit code was zero then return, otherwise raise
    CalledProcessError.  The CalledProcessError object will have the
    return code in the returncode attribute.
    
    The arguments are the same as for the Popen constructor.  Example:
    
    check_call(["ls", "-l"])
    """
    retcode = call(*popenargs, **kwargs)
    if retcode:
        cmd = kwargs.get('args')
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd)
    return 0


def check_output(*popenargs, **kwargs):
    r"""Run command with arguments and return its output as a byte string.
    
    If the exit code was non-zero it raises a CalledProcessError.  The
    CalledProcessError object will have the return code in the returncode
    attribute and output in the output attribute.
    
    The arguments are the same as for the Popen constructor.  Example:
    
    >>> check_output(["ls", "-l", "/dev/null"])
    'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'
    
    The stdout argument is not allowed as it is used internally.
    To capture standard error in the result, use stderr=STDOUT.
    
    >>> check_output(["/bin/sh", "-c",
    ...               "ls -l non_existent_file ; exit 0"],
    ...              stderr=STDOUT)
    'ls: non_existent_file: No such file or directory\n'
    """
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = Popen(stdout=PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get('args')
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd, output=output)
    return output


def list2cmdline(seq):
    """
    Translate a sequence of arguments into a command line
    string, using the same rules as the MS C runtime:
    
    1) Arguments are delimited by white space, which is either a
       space or a tab.
    
    2) A string surrounded by double quotation marks is
       interpreted as a single argument, regardless of white space
       contained within.  A quoted string can be embedded in an
       argument.
    
    3) A double quotation mark preceded by a backslash is
       interpreted as a literal double quotation mark.
    
    4) Backslashes are interpreted literally, unless they
       immediately precede a double quotation mark.
    
    5) If backslashes immediately precede a double quotation mark,
       every pair of backslashes is interpreted as a literal
       backslash.  If the number of backslashes is odd, the last
       backslash escapes the next double quotation mark as
       described in rule 3.
    """
    result = []
    needquote = False
    for arg in seq:
        bs_buf = []
        if result:
            result.append(' ')
        needquote = ' ' in arg or '\t' in arg or not arg
        if needquote:
            result.append('"')
        for c in arg:
            if c == '\\':
                bs_buf.append(c)
            elif c == '"':
                result.append('\\' * len(bs_buf) * 2)
                bs_buf = []
                result.append('\\"')
            else:
                if bs_buf:
                    result.extend(bs_buf)
                    bs_buf = []
                result.append(c)

        if bs_buf:
            result.extend(bs_buf)
        if needquote:
            result.extend(bs_buf)
            result.append('"')

    return ''.join(result)


class Popen(object):

    def __init__(self, args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0):
        """Create new Popen instance."""
        _cleanup()
        self._child_created = False
        if not isinstance(bufsize, (int, long)):
            raise TypeError('bufsize must be an integer')
        if mswindows:
            if preexec_fn is not None:
                raise ValueError('preexec_fn is not supported on Windows platforms')
            if close_fds and (stdin is not None or stdout is not None or stderr is not None):
                raise ValueError('close_fds is not supported on Windows platforms if you redirect stdin/stdout/stderr')
        else:
            if startupinfo is not None:
                raise ValueError('startupinfo is only supported on Windows platforms')
            if creationflags != 0:
                raise ValueError('creationflags is only supported on Windows platforms')
        self.stdin = None
        self.stdout = None
        self.stderr = None
        self.pid = None
        self.returncode = None
        self.universal_newlines = universal_newlines
        p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite = self._get_handles(stdin, stdout, stderr)
        self._execute_child(args, executable, preexec_fn, close_fds, cwd, env, universal_newlines, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)
        if mswindows:
            if p2cwrite is not None:
                p2cwrite = msvcrt.open_osfhandle(p2cwrite.Detach(), 0)
            if c2pread is not None:
                c2pread = msvcrt.open_osfhandle(c2pread.Detach(), 0)
            if errread is not None:
                errread = msvcrt.open_osfhandle(errread.Detach(), 0)
        if p2cwrite is not None:
            self.stdin = os.fdopen(p2cwrite, 'wb', bufsize)
        if c2pread is not None:
            if universal_newlines:
                self.stdout = os.fdopen(c2pread, 'rU', bufsize)
            else:
                self.stdout = os.fdopen(c2pread, 'rb', bufsize)
        if errread is not None:
            if universal_newlines:
                self.stderr = os.fdopen(errread, 'rU', bufsize)
            else:
                self.stderr = os.fdopen(errread, 'rb', bufsize)
        return

    def _translate_newlines(self, data):
        data = data.replace('\r\n', '\n')
        data = data.replace('\r', '\n')
        return data

    def __del__(self, _maxint=sys.maxint, _active=_active):
        if not self._child_created:
            return
        else:
            self._internal_poll(_deadstate=_maxint)
            if self.returncode is None and _active is not None:
                _active.append(self)
            return

    def communicate(self, input=None):
        """Interact with process: Send data to stdin.  Read data from
        stdout and stderr, until end-of-file is reached.  Wait for
        process to terminate.  The optional input argument should be a
        string to be sent to the child process, or None, if no data
        should be sent to the child.
        
        communicate() returns a tuple (stdout, stderr)."""
        if [
         self.stdin, self.stdout, self.stderr].count(None) >= 2:
            stdout = None
            stderr = None
            if self.stdin:
                if input:
                    try:
                        self.stdin.write(input)
                    except IOError as e:
                        if e.errno != errno.EPIPE and e.errno != errno.EINVAL:
                            raise

                self.stdin.close()
            elif self.stdout:
                stdout = self.stdout.read()
                self.stdout.close()
            elif self.stderr:
                stderr = self.stderr.read()
                self.stderr.close()
            self.wait()
            return (
             stdout, stderr)
        else:
            return self._communicate(input)

    def poll(self):
        return self._internal_poll()

    if mswindows:

        def _get_handles(self, stdin, stdout, stderr):
            """Construct and return tuple with IO objects:
            p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
            """
            if stdin is None and stdout is None and stderr is None:
                return (None, None, None, None, None, None)
            else:
                p2cread, p2cwrite = (None, None)
                c2pread, c2pwrite = (None, None)
                errread, errwrite = (None, None)
                if stdin is None:
                    p2cread = _subprocess.GetStdHandle(_subprocess.STD_INPUT_HANDLE)
                    if p2cread is None:
                        p2cread, _ = _subprocess.CreatePipe(None, 0)
                elif stdin == PIPE:
                    p2cread, p2cwrite = _subprocess.CreatePipe(None, 0)
                elif isinstance(stdin, int):
                    p2cread = msvcrt.get_osfhandle(stdin)
                else:
                    p2cread = msvcrt.get_osfhandle(stdin.fileno())
                p2cread = self._make_inheritable(p2cread)
                if stdout is None:
                    c2pwrite = _subprocess.GetStdHandle(_subprocess.STD_OUTPUT_HANDLE)
                    if c2pwrite is None:
                        _, c2pwrite = _subprocess.CreatePipe(None, 0)
                elif stdout == PIPE:
                    c2pread, c2pwrite = _subprocess.CreatePipe(None, 0)
                elif isinstance(stdout, int):
                    c2pwrite = msvcrt.get_osfhandle(stdout)
                else:
                    c2pwrite = msvcrt.get_osfhandle(stdout.fileno())
                c2pwrite = self._make_inheritable(c2pwrite)
                if stderr is None:
                    errwrite = _subprocess.GetStdHandle(_subprocess.STD_ERROR_HANDLE)
                    if errwrite is None:
                        _, errwrite = _subprocess.CreatePipe(None, 0)
                elif stderr == PIPE:
                    errread, errwrite = _subprocess.CreatePipe(None, 0)
                elif stderr == STDOUT:
                    errwrite = c2pwrite
                elif isinstance(stderr, int):
                    errwrite = msvcrt.get_osfhandle(stderr)
                else:
                    errwrite = msvcrt.get_osfhandle(stderr.fileno())
                errwrite = self._make_inheritable(errwrite)
                return (
                 p2cread, p2cwrite,
                 c2pread, c2pwrite,
                 errread, errwrite)

        def _make_inheritable(self, handle):
            """Return a duplicate of handle, which is inheritable"""
            return _subprocess.DuplicateHandle(_subprocess.GetCurrentProcess(), handle, _subprocess.GetCurrentProcess(), 0, 1, _subprocess.DUPLICATE_SAME_ACCESS)

        def _find_w9xpopen(self):
            """Find and return absolut path to w9xpopen.exe"""
            w9xpopen = os.path.join(os.path.dirname(_subprocess.GetModuleFileName(0)), 'w9xpopen.exe')
            if not os.path.exists(w9xpopen):
                w9xpopen = os.path.join(os.path.dirname(sys.exec_prefix), 'w9xpopen.exe')
                if not os.path.exists(w9xpopen):
                    raise RuntimeError('Cannot locate w9xpopen.exe, which is needed for Popen to work with your shell or platform.')
            return w9xpopen

        def _execute_child(self, args, executable, preexec_fn, close_fds, cwd, env, universal_newlines, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite):
            """Execute program (MS Windows version)"""
            if not isinstance(args, types.StringTypes):
                args = list2cmdline(args)
            if startupinfo is None:
                startupinfo = STARTUPINFO()
            if None not in (p2cread, c2pwrite, errwrite):
                startupinfo.dwFlags |= _subprocess.STARTF_USESTDHANDLES
                startupinfo.hStdInput = p2cread
                startupinfo.hStdOutput = c2pwrite
                startupinfo.hStdError = errwrite
            if shell:
                startupinfo.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = _subprocess.SW_HIDE
                comspec = os.environ.get('COMSPEC', 'cmd.exe')
                args = '{} /c "{}"'.format(comspec, args)
                if _subprocess.GetVersion() >= 2147483648 or os.path.basename(comspec).lower() == 'command.com':
                    w9xpopen = self._find_w9xpopen()
                    args = '"%s" %s' % (w9xpopen, args)
                    creationflags |= _subprocess.CREATE_NEW_CONSOLE
            try:
                try:
                    hp, ht, pid, tid = _subprocess.CreateProcess(executable, args, None, None, int(not close_fds), creationflags, env, cwd, startupinfo)
                except pywintypes.error as e:
                    raise WindowsError(*e.args)

            finally:
                if p2cread is not None:
                    p2cread.Close()
                if c2pwrite is not None:
                    c2pwrite.Close()
                if errwrite is not None:
                    errwrite.Close()

            self._child_created = True
            self._handle = hp
            self.pid = pid
            ht.Close()
            return

        def _internal_poll(self, _deadstate=None, _WaitForSingleObject=_subprocess.WaitForSingleObject, _WAIT_OBJECT_0=_subprocess.WAIT_OBJECT_0, _GetExitCodeProcess=_subprocess.GetExitCodeProcess):
            """Check if child process has terminated.  Returns returncode
            attribute.
            
            This method is called by __del__, so it can only refer to objects
            in its local scope.
            
            """
            if self.returncode is None:
                if _WaitForSingleObject(self._handle, 0) == _WAIT_OBJECT_0:
                    self.returncode = _GetExitCodeProcess(self._handle)
            return self.returncode

        def wait(self):
            """Wait for child process to terminate.  Returns returncode
            attribute."""
            if self.returncode is None:
                _subprocess.WaitForSingleObject(self._handle, _subprocess.INFINITE)
                self.returncode = _subprocess.GetExitCodeProcess(self._handle)
            return self.returncode

        def _readerthread(self, fh, buffer):
            buffer.append(fh.read())

        def _communicate(self, input):
            stdout = None
            stderr = None
            if self.stdout:
                stdout = []
                stdout_thread = threading.Thread(target=self._readerthread, args=(
                 self.stdout, stdout))
                stdout_thread.setDaemon(True)
                stdout_thread.start()
            if self.stderr:
                stderr = []
                stderr_thread = threading.Thread(target=self._readerthread, args=(
                 self.stderr, stderr))
                stderr_thread.setDaemon(True)
                stderr_thread.start()
            if self.stdin:
                if input is not None:
                    try:
                        self.stdin.write(input)
                    except IOError as e:
                        if e.errno != errno.EPIPE:
                            raise

                self.stdin.close()
            if self.stdout:
                stdout_thread.join()
            if self.stderr:
                stderr_thread.join()
            if stdout is not None:
                stdout = stdout[0]
            if stderr is not None:
                stderr = stderr[0]
            if self.universal_newlines and hasattr(file, 'newlines'):
                if stdout:
                    stdout = self._translate_newlines(stdout)
                if stderr:
                    stderr = self._translate_newlines(stderr)
            self.wait()
            return (
             stdout, stderr)

        def send_signal(self, sig):
            """Send a signal to the process
            """
            if sig == signal.SIGTERM:
                self.terminate()
            elif sig == signal.CTRL_C_EVENT:
                os.kill(self.pid, signal.CTRL_C_EVENT)
            elif sig == signal.CTRL_BREAK_EVENT:
                os.kill(self.pid, signal.CTRL_BREAK_EVENT)
            else:
                raise ValueError('Unsupported signal: {}'.format(sig))

        def terminate(self):
            """Terminates the process
            """
            _subprocess.TerminateProcess(self._handle, 1)

        kill = terminate
    else:

        def _get_handles(self, stdin, stdout, stderr):
            """Construct and return tuple with IO objects:
            p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
            """
            p2cread, p2cwrite = (None, None)
            c2pread, c2pwrite = (None, None)
            errread, errwrite = (None, None)
            if stdin is None:
                pass
            elif stdin == PIPE:
                p2cread, p2cwrite = os.pipe()
            elif isinstance(stdin, int):
                p2cread = stdin
            else:
                p2cread = stdin.fileno()
            if stdout is None:
                pass
            elif stdout == PIPE:
                c2pread, c2pwrite = os.pipe()
            elif isinstance(stdout, int):
                c2pwrite = stdout
            else:
                c2pwrite = stdout.fileno()
            if stderr is None:
                pass
            elif stderr == PIPE:
                errread, errwrite = os.pipe()
            elif stderr == STDOUT:
                errwrite = c2pwrite
            elif isinstance(stderr, int):
                errwrite = stderr
            else:
                errwrite = stderr.fileno()
            return (
             p2cread, p2cwrite,
             c2pread, c2pwrite,
             errread, errwrite)

        def _set_cloexec_flag(self, fd, cloexec=True):
            try:
                cloexec_flag = fcntl.FD_CLOEXEC
            except AttributeError:
                cloexec_flag = 1

            old = fcntl.fcntl(fd, fcntl.F_GETFD)
            if cloexec:
                fcntl.fcntl(fd, fcntl.F_SETFD, old | cloexec_flag)
            else:
                fcntl.fcntl(fd, fcntl.F_SETFD, old & ~cloexec_flag)

        def _close_fds(self, but):
            if hasattr(os, 'closerange'):
                os.closerange(3, but)
                os.closerange(but + 1, MAXFD)
            else:
                for i in xrange(3, MAXFD):
                    if i == but:
                        continue
                    try:
                        os.close(i)
                    except:
                        pass

        def _execute_child(self, args, executable, preexec_fn, close_fds, cwd, env, universal_newlines, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite):
            """Execute program (POSIX version)"""
            if isinstance(args, types.StringTypes):
                args = [
                 args]
            else:
                args = list(args)
            if shell:
                args = [
                 '/bin/sh', '-c'] + args
                if executable:
                    args[0] = executable
            if executable is None:
                executable = args[0]
            errpipe_read, errpipe_write = os.pipe()
            try:
                try:
                    self._set_cloexec_flag(errpipe_write)
                    gc_was_enabled = gc.isenabled()
                    gc.disable()
                    try:
                        self.pid = os.fork()
                    except:
                        if gc_was_enabled:
                            gc.enable()
                        raise

                    self._child_created = True
                    if self.pid == 0:
                        try:
                            if p2cwrite is not None:
                                os.close(p2cwrite)
                            if c2pread is not None:
                                os.close(c2pread)
                            if errread is not None:
                                os.close(errread)
                            os.close(errpipe_read)

                            def _dup2(a, b):
                                if a == b:
                                    self._set_cloexec_flag(a, False)
                                elif a is not None:
                                    os.dup2(a, b)
                                return

                            _dup2(p2cread, 0)
                            _dup2(c2pwrite, 1)
                            _dup2(errwrite, 2)
                            closed = {
                             None}
                            for fd in [p2cread, c2pwrite, errwrite]:
                                if fd not in closed and fd > 2:
                                    os.close(fd)
                                    closed.add(fd)

                            if close_fds:
                                self._close_fds(but=errpipe_write)
                            if cwd is not None:
                                os.chdir(cwd)
                            if preexec_fn:
                                preexec_fn()
                            if env is None:
                                os.execvp(executable, args)
                            else:
                                os.execvpe(executable, args, env)
                        except:
                            exc_type, exc_value, tb = sys.exc_info()
                            exc_lines = traceback.format_exception(exc_type, exc_value, tb)
                            exc_value.child_traceback = ''.join(exc_lines)
                            os.write(errpipe_write, pickle.dumps(exc_value))

                        os._exit(255)
                    if gc_was_enabled:
                        gc.enable()
                finally:
                    os.close(errpipe_write)

                if p2cread is not None and p2cwrite is not None:
                    os.close(p2cread)
                if c2pwrite is not None and c2pread is not None:
                    os.close(c2pwrite)
                if errwrite is not None and errread is not None:
                    os.close(errwrite)
                data = _eintr_retry_call(os.read, errpipe_read, 1048576)
            finally:
                os.close(errpipe_read)

            if data != '':
                try:
                    _eintr_retry_call(os.waitpid, self.pid, 0)
                except OSError as e:
                    if e.errno != errno.ECHILD:
                        raise

                child_exception = pickle.loads(data)
                for fd in (p2cwrite, c2pread, errread):
                    if fd is not None:
                        os.close(fd)

                raise child_exception
            return

        def _handle_exitstatus(self, sts, _WIFSIGNALED=os.WIFSIGNALED, _WTERMSIG=os.WTERMSIG, _WIFEXITED=os.WIFEXITED, _WEXITSTATUS=os.WEXITSTATUS):
            if _WIFSIGNALED(sts):
                self.returncode = -_WTERMSIG(sts)
            elif _WIFEXITED(sts):
                self.returncode = _WEXITSTATUS(sts)
            else:
                raise RuntimeError('Unknown child exit status!')

        def _internal_poll(self, _deadstate=None, _waitpid=os.waitpid, _WNOHANG=os.WNOHANG, _os_error=os.error):
            """Check if child process has terminated.  Returns returncode
            attribute.
            
            This method is called by __del__, so it cannot reference anything
            outside of the local scope (nor can any methods it calls).
            
            """
            if self.returncode is None:
                try:
                    pid, sts = _waitpid(self.pid, _WNOHANG)
                    if pid == self.pid:
                        self._handle_exitstatus(sts)
                except _os_error:
                    if _deadstate is not None:
                        self.returncode = _deadstate

            return self.returncode

        def wait(self):
            """Wait for child process to terminate.  Returns returncode
            attribute."""
            if self.returncode is None:
                try:
                    pid, sts = _eintr_retry_call(os.waitpid, self.pid, 0)
                except OSError as e:
                    if e.errno != errno.ECHILD:
                        raise
                    sts = 0

                self._handle_exitstatus(sts)
            return self.returncode

        def _communicate(self, input):
            if self.stdin:
                self.stdin.flush()
                if not input:
                    self.stdin.close()
            if _has_poll:
                stdout, stderr = self._communicate_with_poll(input)
            else:
                stdout, stderr = self._communicate_with_select(input)
            if stdout is not None:
                stdout = ''.join(stdout)
            if stderr is not None:
                stderr = ''.join(stderr)
            if self.universal_newlines and hasattr(file, 'newlines'):
                if stdout:
                    stdout = self._translate_newlines(stdout)
                if stderr:
                    stderr = self._translate_newlines(stderr)
            self.wait()
            return (
             stdout, stderr)

        def _communicate_with_poll(self, input):
            stdout = None
            stderr = None
            fd2file = {}
            fd2output = {}
            poller = select.poll()

            def register_and_append(file_obj, eventmask):
                poller.register(file_obj.fileno(), eventmask)
                fd2file[file_obj.fileno()] = file_obj

            def close_unregister_and_remove(fd):
                poller.unregister(fd)
                fd2file[fd].close()
                fd2file.pop(fd)

            if self.stdin and input:
                register_and_append(self.stdin, select.POLLOUT)
            select_POLLIN_POLLPRI = select.POLLIN | select.POLLPRI
            if self.stdout:
                register_and_append(self.stdout, select_POLLIN_POLLPRI)
                fd2output[self.stdout.fileno()] = stdout = []
            if self.stderr:
                register_and_append(self.stderr, select_POLLIN_POLLPRI)
                fd2output[self.stderr.fileno()] = stderr = []
            input_offset = 0
            while fd2file:
                try:
                    ready = poller.poll()
                except select.error as e:
                    if e.args[0] == errno.EINTR:
                        continue
                    raise

                for fd, mode in ready:
                    if mode & select.POLLOUT:
                        chunk = input[input_offset:input_offset + _PIPE_BUF]
                        try:
                            input_offset += os.write(fd, chunk)
                        except OSError as e:
                            if e.errno == errno.EPIPE:
                                close_unregister_and_remove(fd)
                            else:
                                raise
                        else:
                            if input_offset >= len(input):
                                close_unregister_and_remove(fd)
                    elif mode & select_POLLIN_POLLPRI:
                        data = os.read(fd, 4096)
                        if not data:
                            close_unregister_and_remove(fd)
                        fd2output[fd].append(data)
                    else:
                        close_unregister_and_remove(fd)

            return (
             stdout, stderr)

        def _communicate_with_select(self, input):
            read_set = []
            write_set = []
            stdout = None
            stderr = None
            if self.stdin and input:
                write_set.append(self.stdin)
            if self.stdout:
                read_set.append(self.stdout)
                stdout = []
            if self.stderr:
                read_set.append(self.stderr)
                stderr = []
            input_offset = 0
            while read_set or write_set:
                try:
                    rlist, wlist, xlist = select.select(read_set, write_set, [])
                except select.error as e:
                    if e.args[0] == errno.EINTR:
                        continue
                    raise

                if self.stdin in wlist:
                    chunk = input[input_offset:input_offset + _PIPE_BUF]
                    try:
                        bytes_written = os.write(self.stdin.fileno(), chunk)
                    except OSError as e:
                        if e.errno == errno.EPIPE:
                            self.stdin.close()
                            write_set.remove(self.stdin)
                        else:
                            raise
                    else:
                        input_offset += bytes_written
                        if input_offset >= len(input):
                            self.stdin.close()
                            write_set.remove(self.stdin)
                if self.stdout in rlist:
                    data = os.read(self.stdout.fileno(), 1024)
                    if data == '':
                        self.stdout.close()
                        read_set.remove(self.stdout)
                    stdout.append(data)
                if self.stderr in rlist:
                    data = os.read(self.stderr.fileno(), 1024)
                    if data == '':
                        self.stderr.close()
                        read_set.remove(self.stderr)
                    stderr.append(data)

            return (stdout, stderr)

        def send_signal(self, sig):
            """Send a signal to the process
            """
            os.kill(self.pid, sig)

        def terminate(self):
            """Terminate the process with SIGTERM
            """
            self.send_signal(signal.SIGTERM)

        def kill(self):
            """Kill the process with SIGKILL
            """
            self.send_signal(signal.SIGKILL)


def _demo_posix():
    plist = Popen(['ps'], stdout=PIPE).communicate()[0]
    print 'Process list:'
    print plist
    if os.getuid() == 0:
        p = Popen(['id'], preexec_fn=lambda : os.setuid(100))
        p.wait()
    print "Looking for 'hda'..."
    p1 = Popen(['dmesg'], stdout=PIPE)
    p2 = Popen(['grep', 'hda'], stdin=p1.stdout, stdout=PIPE)
    print repr(p2.communicate()[0])
    print
    print 'Trying a weird file...'
    try:
        print Popen(['/this/path/does/not/exist']).communicate()
    except OSError as e:
        if e.errno == errno.ENOENT:
            print "The file didn't exist.  I thought so..."
            print 'Child traceback:'
            print e.child_traceback
        else:
            print 'Error', e.errno
    else:
        print >> sys.stderr, 'Gosh.  No error.'


def _demo_windows():
    print "Looking for 'PROMPT' in set output..."
    p1 = Popen('set', stdout=PIPE, shell=True)
    p2 = Popen('find "PROMPT"', stdin=p1.stdout, stdout=PIPE)
    print repr(p2.communicate()[0])
    print 'Executing calc...'
    p = Popen('calc')
    p.wait()


if __name__ == '__main__':
    if mswindows:
        _demo_windows()
    else:
        _demo_posix()