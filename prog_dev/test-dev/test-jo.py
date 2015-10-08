#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#

from time import sleep
import select
import signal
import fcntl
import os
import sys

def dopoll(poller):
    while True:
        try:
            return poller.poll()
        except IOError as e:
            if e.errno != EINTR:
                raise

def main():
    pipe_r, pipe_w = os.pipe()
    flags = fcntl.fcntl(pipe_w, fcntl.F_GETFL, 0)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(pipe_w, fcntl.F_SETFL, flags)
    
    signal.signal(signal.SIGCHLD, lambda x,y: None)
    signal.signal(signal.SIGALRM, lambda x,y: None)
    signal.siginterrupt(signal.SIGCHLD,False) #makes no difference
    signal.siginterrupt(signal.SIGALRM,False) #makes no difference
    signal.set_wakeup_fd(pipe_w)
    signal.setitimer(signal.ITIMER_REAL, 2, 2)
    
    poller = select.epoll()
    poller.register(pipe_r, select.EPOLLIN)
    poller.register(sys.stdin, select.EPOLLIN)
    
    print "Main screen turn on"
    while True:
        events=[]
        try:
            events = poller.poll()
            try:
                for fd, flags in events:
                    ch=os.read(fd, 1)
                    if fd==pipe_r:
                        sys.stdout.write( "We get Signal" )
                    if fd==sys.stdin.fileno():
                        sys.stdout.write( ch )
                    sys.stdout.flush()
            except IOError as e:
                print "exception loop" + str(e)
        except IOError as e:
            print "exception poll" + str(e)


if __name__ == '__main__':
    main()
