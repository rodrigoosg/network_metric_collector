#!/usr/bin/python

from nmc.procnetdev import ProcNetDev
import time
import sys

if __name__ == "__main__":

	while True:
		pnd = ProcNetDev()
		last_time  = time.time()
		last_bytes = pnd['eth0']['receive']['bytes'] 
		time.sleep(1)
	    now_bytes = pnd['eth0']['receive']['bytes']
		print "Bytes Received: %s B/s" % (int(now_bytes) - int(last_bytes))
		sys.stdout.flush()
