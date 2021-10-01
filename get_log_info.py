import os
import sys
import time
import sh
import subprocess
import select


file_name = "/media/bob/ssd128/event.log"
data = sh.tail('-f','/media/bob/ssd128/event.log',_iter=True)
#f = subprocess.Popen(["tail", "-F",file_name],\stout=subprocess.PIPE,stderr=subprocess.PIPE)
#print(data, ..., sep=' ', end='\n', file=sys.stdout, flush=False)
#p = select.poll()
#p.register(f.stout)

while True:
	#line = f.stdout.readline()
	data1 = []
	data1 = data.next()
	data1 = data1.rstrip()
	data1 = data1.split('-')
	#print(data, ..., sep=' ', end='\n', file=sys.stdout, flush=False)
	print(data1[3])

