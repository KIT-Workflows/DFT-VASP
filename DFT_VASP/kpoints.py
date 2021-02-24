import pymatgen
from pymatgen.core.structure import Structure, Lattice
from pymatgen.io.vasp import Incar, Poscar, Potcar, Kpoints
import os, sys, re


#kpoints = Kpoints.gamma_automatic([3, 3, 3], [0, 0, 0])
#kpoints = Kpoints.monkhorst_automatic([3, 3, 3], [0, 0, 0])
#kpoints = Kpoints.automatic(50)
#poscar = Poscar.from_file("POSCAR")
#kpoints = Kpoints.automatic_density(poscar.structure, 500, True)

args = sys.argv[1:]

#print(args)

Rk = args[0]
Rk_val = int(args[1])
Monkhorst = args[2]
n = [int(args[5]), int(args[7]), int(args[9])]
n_shift = [float(args[13]), float(args[15]), float(args[17])]

# print(Rk)
# print(type(n))
# print(type(n_shift))
# print(args[0])

if  Rk == 'True':
    kpoints = Kpoints.automatic(Rk_val)
elif Monkhorst == 'True':
    kpoints = Kpoints.monkhorst_automatic(n, n_shift)
    # kpoints = Kpoints.gamma_automatic(n, n_shift)
else:
    None

kpoints.write_file('KPOINTS')
print("KPOINTS successfully created")