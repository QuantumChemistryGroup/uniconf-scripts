#!/usr/bin/python
import sys, string
from math import *

f = open(sys.argv[1])

s = f.readline()
i = 0
for line in f:  # for each line in a file
	if 'CHELPG Charges' in line: i = i + 1   
print (i)

f.seek(0)
s = f.readline()



for j in range(i):
	while str.find(s, 'CHELPG Charges') == -1 and s != "": s = f.readline()
	s = f.readline()

s = f.readline()

Z = []

while str.find(s, "--------") == -1:
	d = str.split(s); 
	if len(d) == 4:
		z = float(d[3])
		Z.append(z)
		s = f.readline()
	else: print ("All the charges read"); s = f.readline()

f.close()

f = open(sys.argv[1][0:-4]+'.chr', 'w')
for i in Z:
	f.write(str(i)+'\n')
f.close()
