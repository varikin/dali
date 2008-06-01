#!/usr/bin/env python

import subprocess
import os
import os.path
import signal

django_dir = "/Users/varikin/code/blag/iox/"
lighty_dir = "/Users/varikin/lighttpd/"
lighty_conf = lighty_dir + "lighttpd.conf"
django_pid = django_dir + "django.pid"
lighty_pid = lighty_dir + "lighty.pid"
django_logs = django_dir + "logs/"
django_stdout = django_logs + "stdout.log"
django_stderr = django_logs + "stderr.log"

def readPid(filename):
	f = open(filename)
	pid = int(f.readline())
	f.close()
	return pid

def stopServer(pidfile):
	if(os.path.exists(pidfile)):
		pid = readPid(pidfile)
		os.kill(pid, signal.SIGTERM)
		os.remove(pidfile)	

def startServer(cmd):
	fcgi = subprocess.Popen((cmd))
			
django_cmd = (django_dir + "manage.py", "runfcgi", "method=threaded", "host=127.0.0.1", "port=3033", "pidfile=" + django_pid, "outlog=" + django_stdout, "errlog=" + django_stderr)
lighty_cmd = (lighty_dir + "sbin/lighttpd", "-f", lighty_conf)

stopServer(lighty_pid)
stopServer(django_pid)
startServer(django_cmd)
startServer(lighty_cmd)
