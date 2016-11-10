#!/usr/bin/python

from nmc.procnetdev import ProcNetDev
import time
from time import gmtime, strftime
import sys
import schedule

last_bytes = 0

def job():
	global last_bytes
	pnd = ProcNetDev()
	tmp_bytes = last_bytes
	last_bytes = pnd['eth0']['transmit']['bytes']
	delta_bytes = last_bytes - tmp_bytes 
	now = strftime("%Y/%m/%dT%H:%M:%S", gmtime())
	print "Time: %s | Bytes Transmitted: %s B/s" % (now, int(delta_bytes))
	sys.stdout.flush()

if __name__ == "__main__":
	schedule.every(1).minute.do(job)
	while True:
		schedule.run_pending()
		time.sleep(1)
