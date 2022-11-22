#import numpy as np
import re, os
#import pymatgen
# import pymatgen.io.vasp.sets 
# from pymatgen import Lattice
# from pymatgen import Structure, Molecule

def clean_num(srt_var):
    alphanumeric_filter = filter(str.isalnum, srt_var)
    alphanumeric_string = "".join(alphanumeric_filter)
    return alphanumeric_string
def clean_tuple(my_list):
    my_list = [clean_num(i) for i in my_list]
    my_list = list(filter(None, my_list))
    my_list = [int(i) for i in my_list]
    my_list =  tuple(my_list)
    return my_list

def read_elements(filename):
    with open(filename) as f:
        Var1 = f.read().splitlines()
        Var2 = Var1[5]
    Chem_elem_temp = re.split("\s+", Var2)
    Chem_elem = [string for string in Chem_elem_temp if string != ""]

    print(Chem_elem)
    return Chem_elem

def gen_potcar(var_elements):
    var_path = "/shared/software/chem/vasp/potpaw_PBE.54/"
    var_pot_GW = "_GW/POTCAR"
    pot_var = ""
    
    x_d = ["Pb", "Sb", "Sn"]
    x_sv = ["Cs", "K", "Rb", "Na", "Nb", "Ba", "Mo"]

    for i in var_elements:
        if i in x_d:
            pot_var = pot_var + var_path + i + "_d" + var_pot_GW + " "
        elif i in x_sv:
            pot_var = pot_var + var_path + i + "_sv" + var_pot_GW + " "
        else:
            pot_var = pot_var + var_path + i + var_pot_GW + " "
    
    os.system("cat " + pot_var + " > POTCAR")
    print(pot_var)
    print("POTCAR generate for:", var_elements)
    
#file_poscar = Structure.from_file("POSCAR")
if os.path.isfile('POTCAR'):
    print("POTCAR already loaded")
    exit
else:
    potcar_elements = read_elements("POSCAR")
    gen_potcar(potcar_elements)