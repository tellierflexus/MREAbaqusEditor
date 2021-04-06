import re
import argparse
import sys

parser = argparse.ArgumentParser(description='Edit an abaqus input file to add magnetic behavior of materials')
parser.add_argument('file', action='store', help='Specify the name of the input file')
parser.add_argument('--dummy', const=True, default=False, action='store_const', help='Add a dummy mesh')
parser.add_argument('--magFieldMag', default='0.01', action='store', help='Magnitude of the magnetic field')
parser.add_argument('--magFieldVecX', default='0.0', action='store', help='X component of the unit vector magnetic field')
parser.add_argument('--magFieldVecY', default='-1.0', action='store', help='Y component of the unit vector magnetic field')
parser.add_argument('--magFieldVecZ', default='0.0', action='store', help='Z component of the unit vector magnetic field')

parser.add_argument('--Mx', default='0.0', action='store', help='X component of the initial magnetic moment density')
parser.add_argument('--My', default='-1.0', action='store', help='Y component of the initial magnetic moment density')
parser.add_argument('--Mz', default='-94.06e3', action='store', help='Z component of the initial magnetic moment density')
parser.add_argument('--Gshear', default='400e3', action='store', help='X component of the unit vector magnetic field')
parser.add_argument('--Kbulk', default='400e5', action='store', help='Y component of the unit vector magnetic field')

args = parser.parse_args()

try:
	with open(args.file, 'r') as inp_file:
		content = inp_file.read()
except FileNotFoundError:
	print("The file specified cannot be found")
	exit()
except:
	print("Unexpected error:", sys.exc_info()[0])
	raise


"""


		Text template



"""
parameters = """************************************************************************
*Parameter
** 
** final magnitude of the applied magnetic field (Tesla)
magFieldMag = $magFieldMag$
**
** applied magnetic field unit vector
magFieldVecX = $magFieldVecX$
magFieldVecY = $magFieldVecY$
magFieldVecZ = $magFieldVecZ$
**
**	MATERIAL PARAMETERS 
**
** initial magnetic moment density (A/m)
Mx = $Mx$
My = $My$
Mz = $Mz$
**
** initial shear modulus (Pa)
Gshear = $Gshear$
**
** bulk modulus (Pa)
Kbulk = $Kbulk$
**
** number of body integration points
nInt = 8
**
** number of real material properties
nProps = 5
**
** number of integer material properties
nJProps = 1
**
************************************************************************\n""";

element = """************************************************************************
*User Element,Nodes=8,Type=U3,Iproperties=<nJProps>,Properties=<nProps>,Coordinates=3,Unsymm
1,2,3
************************************************************************
*Element, type=U3"""

dummy_mesh = "*Elset, elset=$elset$_dummy_mesh, generate\n10001, $LastDummyElement$, 1\n"
"""


		Preparation of template



"""
parameters = re.sub(r'(?:[$]magFieldMag[$])', args.magFieldMag,parameters)
parameters = re.sub(r'(?:[$]magFieldVecX[$])', args.magFieldVecX,parameters)
parameters = re.sub(r'(?:[$]magFieldVecY[$])', args.magFieldVecY,parameters)
parameters = re.sub(r'(?:[$]magFieldVecZ[$])', args.magFieldVecZ,parameters)
parameters = re.sub(r'(?:[$]Mx[$])', args.Mx,parameters)
parameters = re.sub(r'(?:[$]My[$])', args.My,parameters)
parameters = re.sub(r'(?:[$]Mz[$])', args.Mz,parameters)
parameters = re.sub(r'(?:[$]Gshear[$])', args.Gshear,parameters)
parameters = re.sub(r'(?:[$]Kbulk[$])', args.Kbulk,parameters)

match = re.search(r'(?:[*]Elset,\selset=([^,]{1,}),\sgenerate\s+([0-9]+),\s+([0-9]+))', content)
if match:
	elset = match.expand(r'\1')
	nbrOfElem = int(match.expand(r'\3')) -int(match.expand(r'\2'))
	print(elset)
	print(nbrOfElem)
else: 
	print("No elset found, exiting...")
	exit()

match = re.search(r'(?:[*]Instance,\sname=(.+),)', content)
if match:
	Instance = match.expand(r'\1')
	print(Instance)
else: 
	print("No Instance found, exiting...")
	exit()

dummy_mesh = re.sub(r'(?:[$]LastDummyElement[$])', str(10001 + nbrOfElem), dummy_mesh)
dummy_mesh = re.sub(r'(?:[$]elset[$])', elset, dummy_mesh)
"""


		Insertion of template



"""

content = re.sub(r'((?:[*]{2}\s[*]{2}\sPARTS\n))', parameters + r'\1', content)
content = re.sub(r'(?:[*]Element,\stype=C3D8RH)',element, content)
if (~args.dummy):
	dummy_mesh=''
print(args.dummy)
content = re.sub(r'(?:[*]{2}\sSection:.+\s.+\s,\s)', dummy_mesh, content)

print(content)