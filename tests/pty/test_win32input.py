#!/usr/bin/env python3
"""The win32 input mode of TvUnix in a pty: usage: test_win32input.py PROGRAM (tvdemo).
TV_WIN32_INPUT=1: the program asks for the mode (ESC [ ? 9001 h), understands Alt-X sent as
"ESC [ Vk ; Sc ; Uc ; Kd ; Cs ; Rc _", ends and switches the mode off (ESC [ ? 9001 l).
TV_WIN32_INPUT=0: it does not ask. Prints ALL OK."""
import os, pty, select, sys, time

def run(prog, env_value, send):
    env = dict(os.environ, TERM='xterm-256color', TV_WIN32_INPUT=env_value)
    env.pop('WT_SESSION', None)
    pid, fd = pty.fork()
    if pid == 0:
        os.execve(prog, [prog], env)
    out = b''
    def pump(sec):
        nonlocal out
        end = time.time() + sec
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if r:
                try:
                    d = os.read(fd, 65536)
                except OSError:
                    return False
                if not d:
                    return False
                out += d
        return True
    pump(1.5)
    if send:
        os.write(fd, send)
        pump(1.5)
    try:
        done, _ = os.waitpid(pid, os.WNOHANG)
    except ChildProcessError:
        done = pid
    if not done:
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    return out, bool(done)

prog = os.path.abspath(sys.argv[1])
fail = 0
def check(ok, msg):
    global fail
    print(('PASS ' if ok else 'FAIL ') + msg)
    fail += 0 if ok else 1

out, ended = run(prog, '1', b'\x1b[88;45;120;1;2;1_\x1b[88;45;120;0;2;1_')
check(b'\x1b[?9001h' in out, 'TV_WIN32_INPUT=1: the mode is asked for')
check(ended, 'Alt-X in the win32 format ends the program')
check(b'\x1b[?9001l' in out, '... and the mode is switched off')
out, ended = run(prog, '0', None)
check(b'\x1b[?9001h' not in out, 'TV_WIN32_INPUT=0: the mode is not asked for')
print('ALL OK' if not fail else '%d FAILED' % fail)
sys.exit(1 if fail else 0)
