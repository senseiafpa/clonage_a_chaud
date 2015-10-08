#!/usr/bin/env python2.7

import subprocess

# p = subprocess.Popen(['../clone_optimisation/clone_dst_main.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)

p = subprocess.Popen(['ssh', 
		      'root@localhost', 
		      '/media/OS/Users/Jonathan/Desktop/Partages-NFS_Dev-Python/prog_dev/clone_optimisation/clone_dst_main.py'], 
		      stdin=subprocess.PIPE, 
		      stdout=subprocess.PIPE, 
		      close_fds=True)

print p

p.stdin.write("12345678901234567890") # 'hash block' simuler
p.stdin.flush()

out = p.stdout
line = out.readline()
while line != "":
	print line
	line = out.readline()


