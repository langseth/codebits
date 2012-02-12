#!/usr/local/bin/python

import select
from select import kqueue, kevent
from time import sleep
import os
import sys


filename = "access"
fh = open(filename, "r")
kq = kqueue()
event = [
         kevent(fh, filter=select.KQ_FILTER_VNODE,
                flags=select.KQ_EV_ADD | select.KQ_EV_CLEAR,
                fflags=select.KQ_NOTE_DELETE | 
                       select.KQ_NOTE_RENAME |
                       select.KQ_NOTE_WRITE)
        ]
print fh.read(),
kq.control(event,0)
try:
    while True:
        r_events = kq.control(None,1)
        for event in r_events:
            if event.fflags & select.KQ_NOTE_WRITE:
                print fh.read(),
            if event.fflags & select.KQ_NOTE_DELETE:
                kq.close()
                fh.close()
                exit(0)
            elif event.fflags & select.KQ_NOTE_RENAME:
                event.flags = select.KQ_EV_DELETE
                kq.control([event],0,0)
                fh.close()
                sleep(1)
                fh = open(filename,"r")
                kq.control([kevent(fh,
                                   filter=select.KQ_FILTER_VNODE,
                                   flags=select.KQ_EV_ADD |
                                         select.KQ_EV_CLEAR,
                                   fflags=select.KQ_NOTE_DELETE |
                                          select.KQ_NOTE_RENAME |
                                          select.KQ_NOTE_WRITE)],
                           0
                )
            elif event.ident == 1000:
                event.flags = select.KQ_EV_DISABLE
                kq.control([event],0,0)
except KeyboardInterrupt:
    kq.close()
    fh.close()
    exit(1)
