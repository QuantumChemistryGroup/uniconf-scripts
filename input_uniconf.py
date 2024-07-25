#!/usr/bin/python
import sys, string, os, glob
from math import *

# a few special functions
def IsFloat(s):
        try: 
                float(s)
                return True
        except ValueError:
                return False

def IsInt(s):
        try: 
                int(s)
                return True
        except ValueError:
                return False

# script to prepare the input file for the uniconf conformer generator

# reading the file with coordinates & charges

molchr=[]
mol = []

f = open(sys.argv[1], "r")
for line in f:
	d = str.split(line)
	if len(d) == 4 and IsFloat(d[1]) == True and IsFloat(d[2]) == True and IsFloat(d[3]) == True:
		mol.append([d[0], d[1], d[2], d[3]])
f.close()
f = open(sys.argv[1][0:-4]+'.chr', "r")
for line in f:
	d = str.split(line)
	if len(d) == 1 and IsFloat(d[0]) == True:
		molchr.append(d[0])
f.close()

# check

if len(mol) != len(molchr):
	print ("Mismatch between number of coordinates in xyz and chr files %4i %4i" % (len(molxyz), len(molchr)))
	sys.exit(0)
else:
	for i in range(len(mol)):
		mol[i].append(molchr[i])


mode = sys.argv[2].lower()
if mode == 'simple' or mode == 'bonds' or mode == 'quiz':
	pass
else: 
	print ("Please, specify the second argument: \n")
	print ("simple or bonds or quiz\n")
	sys.exit(0) 
# parameters 
bonds = []
numbond = len(bonds)
if mode == 'bonds' or mode == 'quiz':
	numbond = int(input("Enter number of rotatable bonds: "))
	for j in range(numbond):
		bond = str(input("Enter rotatable bond as Atom1 Atom2 Angle_Increment Angle_Max Angle_Dev \n (e.g. 1 2 120 240 15) : "))
		d1 = str.split(bond, ' ')
		d=[]
		for j1 in d1:
			if (IsInt(j1) == True):
				d.append(j1)
		if len(d) == 5 and IsInt(d[0]) == True and IsInt(d[1]) == True and IsInt(d[2]) == True and IsInt(d[3]) == True and IsInt(d[4]) == True:
			for i in range(len(d)):
				d[i] = int(d[i])
			bonds.append(d)
		else:
			print ("Something is wrong, please give 5 int values!")
			sys.exit(0)

# writing the uniconf input

f = open(sys.argv[1][0:-4]+'-uni.inp', 'w')
f.write('$BOND\n')
for i in range(len(bonds)):
	f.write('%5i %5i %5i %5i %5i\n' % (bonds[i][0], bonds[i][1], bonds[i][2], bonds[i][3], bonds[i][4]) )
f.write('$END\n')
f.write('$ALGO\n')
f.write('''ALGO=CONF CONNECT=WRITE library=nlopt optloc=nlopt_ln_sbplx 
MAXDISTDIff=0.1 EDIFF=0.1 DIST=1.3 RMSD=0.05 
STRATEGY=1 SCALE=0.35 CLUSTERPROPERTY=EIXX SORT=e
MK=10000 ITER1=15 KMEANS=300  MAXCONF=1000 COM=0
ITER2=10000 KMEANS1=100 MAXCONFPRINT=5000 
''')
f.write('$END\n')
f.write('$MOLECULE\n')
for i in range(len(mol)):
	f.write('%3s %15s %15s %15s\n' % (mol[i][0], mol[i][1], mol[i][2], mol[i][3]))
f.write('$END\n')
f.write('$CHARGE\n')
for i in range(len(mol)):
	f.write('%12s \n' % mol[i][4])
f.write('$END\n')
f.close()
