#!/usr/local/bin/python

import select
from select import kqueue, kevent
import os
import sys

filename = "foo.txt"


fd = os.open(filename,os.O_RDONLY)

kq = kqueue()

event = [kevent(fd, filter=select.KQ_FILTER_READ, flags=select.KQ_EV_ADD),
         kevent(fd, filter=select.KQ_FILTER_VNODE, flags=select.KQ_EV_ADD | select.KQ_EV_CLEAR,
	        fflags=select.KQ_NOTE_DELETE | select.KQ_NOTE_RENAME),
	 kevent(1000,filter=select.KQ_FILTER_TIMER,
	        flags=select.KQ_EV_ADD | select.KQ_EV_CLEAR, data=1000)]

events = kq.control(event,0,5)

while True:
	print "loop"
	r_events = kq.control(None,4)
	for event in r_events:
		print event
	for event in r_events:
		if event.fflags & select.KQ_NOTE_DELETE:
			print "file was deleted"
		elif event.fflags & select.KQ_NOTE_RENAME:
			print "file was renamed"
			event.flags = select.KQ_EV_CLEAR
			kq.control([event],0,0)
		elif event.ident == 1000:
			event.flags = select.KQ_EV_DISABLE
			kq.control([event],0,0)
kq.close()
os.close(fd)
