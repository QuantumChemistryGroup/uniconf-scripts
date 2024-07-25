#!/usr/bin/python
import sys, string, os, glob
from math import *


# The input files for geometry/sp will be created by using that script
# sys.argv[1] = xyz files

# Main program starts here

f = open(sys.argv[1])
DFT = sys.argv[2]
# coordinates

coord = f.readlines() # read every line

d = str.split(coord[0])
if len(d) == 1:
        MOL = True
else: MOL = False 

if MOL:
        coord = coord[2:]

coordinates = []

for i in coord:
	i = str.split(i)
	if len(i) > 3:
		coordinates.append(i)

#################################
# system requeriments
#################################
cores = int(sys.argv[3])
mem = float(sys.argv[4])
######### Multiplecity

mult = sys.argv[1][1:2]
charge = int(sys.argv[1][3:5])

# all molecule

fil = open(sys.argv[1][0:-4]+'_'+DFT+'_TZ.inp', 'w')

fil.write('%s\n' % ('# put your comments here'))
fil.write('%s\n' % ('%pal nprocs '+str(cores)+' end'))

# check for dispersion correction
DISP = ''
if '-d3' in DFT.lower() and 'b97' not in DFT.lower():
	DISP='D3BJ'
	DFT=DFT[0:-3]
elif '-d4' in DFT.lower() and 'b97' not in DFT.lower():
	DISP='D4'
	DFT=DFT[0:-3]
elif 'wb97' in DFT.lower():
	DISP=''
elif 'm06' in DFT.lower():
	DISP=''
elif '-3c' in DFT.lower():
	DISP=''
elif 'mp2' in DFT.lower():
	DISP=''
else:
	print ('No dispersion correction in your functional. Are you sure?')

if 'ri-scs-mp2' in DFT.lower():
	fil.write('''! '''+DFT+''' def2-tzvpp def2-tzvpp/C SP TightSCF NOTRAH '''+DISP+'''
%scf MaxIter 800 end
''')
else:
	fil.write('''! '''+DFT+''' def2-tzvp SP DEFGRID3 NOTRAH CHELPG '''+DISP+'''
%scf MaxIter 800 end
%output
Print [P_Hirshfeld] 1
end
''')
fil.write('%s\n' % ('%MaxCore '+str(0.75*mem/cores)))
fil.write('* xyz '+str(charge)+' '+str(mult)+'\n')
for i in range(len(coordinates)):
	fil.write('%2s %16s %16s %16s\n' % ( coordinates[i][0], coordinates[i][1], coordinates[i][2], coordinates[i][3]))
fil.write('*\n')

fil.write('\n' % ())
fil.write('\n' % ())
fil.write('\n' % ())
fil.close()








