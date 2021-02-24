import pymatgen
from pymatgen.core.structure import Structure, Lattice
from pymatgen.io.vasp import Incar, Poscar, Potcar, Kpoints
from pymatgen.io.vasp.sets import MPRelaxSet
import os, sys, re, yaml

def get_VASP_inputs(structure):
    #poscar  = Poscar(structure)
    incar_dict = dict(  SYSTEM  =   structure.formula, # Name of the system
                        ## Electronic relaxation:
                        ENCUT   =   500.,        # 500. eV, value for carbon atom
                        NELMIN  = 6,             # Minimum number of eletronic selfconsistency (SC) steps
                        NELM    = 1000,           # Maximum number of electronic SC steps
                        NELMDL  = -12,           # Number of NON-selfconsistency steps
                        EDIFF   = 1.0E-6,        # Global-break condition for the electronic SC-loop (ELM)

                        ## Calculation mode:
                        PREC    = 'NORMAL',      # Calcululation level (Changes FFT-grids)
                        ISPIN   = 2,             # spin-polarized calculations
                        ADDGRID = '.TRUE.',      # level of precision
                        IVDW = 0,                # no vdW corrections
                        
                        ## Ionic relaxation:  
                        NSW     =   150,         # Maximum number of ionic steps
                        EDIFFG  = -0.025,        # stop if all forces are smaller than |EDIFFG|
                        IBRION  = 2,         
                        ISIF    = 3,             # Controls the computation of stress tensor. 3 computes everything
                        POTIM   = 0.010,
                        ## Integration over the Brillouin zone (BZ):
                        ISMEAR  = 0,             # Gaussian smearing scheme. Use 0 for insulators, as suggested by VASPWIKI
                        SIGMA   = 0.010,
                        LREAL   = '.FALSE.',        # Should projections be done in real space? Let VASP decide
                        
                        ## DOS calculation:
                        LORBIT  = 10,            # Calculate the DOS without providing the Wigner Seitz radius
                        NEDOS   =  101,          # Number of points to calculate the DOS
                        ## OUTCAR size:
                        NWRITE  = 1,             # Determines how much information will be written in OUTCAR
                        LCHARG  =  '.FALSE.',    # Write charge densities?
                        LWAVE   =  '.FALSE.',    # write out the wavefunctions?
                        LASPH   = '.TRUE.',      # non-spherical elements in the PAW method
                        
                        ## Key for parallel mode calculation:
                        NCORE   = 4,
                        LPLANE  =   '.TRUE.'     # Plane distribution of FFT coefficients. Reduces communications in FFT.
                     )  
    #incar   = Incar.from_dict(incar_dict )
    #incar.write_file('INCAR')
    return incar_dict

def check_IVDW(dict_INCAR):

    var_value = dict_INCAR.get('IVDW')
    if var_value == "D2":
        var_value = int(10)
    elif var_value == "D3":
        var_value = int(11)
    elif var_value == "D3BJ":
        var_value = int(12)
    elif var_value == "dDsC":
        var_value = int(4)
    elif var_value == "TS":
        var_value = int(20)
    elif var_value == "TSSCS":
        var_value = int(21)
    elif var_value == "MBDSC":
        var_value = int(202)
    else:
        var_value = int(0)
    
    if var_value > 0:
        dict_INCAR['IVDW'] = var_value
        dict_INCAR['ADDGRID'] = '.FALSE.'
        dict_INCAR['LASPH'] = '.FALSE.'
    else:
        dict_INCAR['IVDW'] = var_value    

    return dict_INCAR

def check_SOC(dict_INCAR):
    if "SOC" in dict_INCAR.keys() and dict_INCAR["SOC"] == True:
        dict_INCAR["LASPH"] = ".TRUE."
        dict_INCAR["LSORBIT"] = ".TRUE."
        dict_INCAR["GGA_COMPAT"] = ".TRUE."
        dict_INCAR["SAXIS"] = "0 0 1"    
        dict_INCAR["ISYM"] = 0
    
    del dict_INCAR["SOC"]
    return dict_INCAR

def check_Bader(dict_Analysis, dict_INCAR):
    if "Bader" in dict_Analysis.keys() and dict_Analysis["Bader"] == True:
        print('here2')
        dict_INCAR["LCHARG"] = ".TRUE."
        dict_INCAR["LAECHG"] = ".TRUE."
        dict_INCAR["LREAL"] = "AUTO"
        dict_INCAR["NGXF"]  = dict_Analysis["Mesh"].get("NGXF")  
        dict_INCAR["NGYF"]  = dict_Analysis["Mesh"].get("NGYF")
        dict_INCAR["NGZF"]  = dict_Analysis["Mesh"].get("NGZF")
        
    return dict_INCAR

def check_DOS(dict_Analysis, dict_INCAR):
    if "DOS" in dict_Analysis.keys() and dict_Analysis["DOS"] == True:  
        dict_INCAR["LORBIT"]  = dict_Analysis["dos_calculation"].get("LORBIT")
        dict_INCAR["NEDOS"]  = dict_Analysis["dos_calculation"].get("NEDOS")
        
    return dict_INCAR

structure = Structure.from_file("POSCAR")   
dict_INCAR = get_VASP_inputs(structure)


with open('rendered_wano.yml') as file:
    wano_file = yaml.full_load(file)


# Reading the inputs for INCAR file
for var_key, var_value in wano_file["TABS"]["INCAR"].items():
    if var_key in dict_INCAR.keys():
        dict_INCAR[var_key] = var_value
    else:
        dict_INCAR[var_key] = var_value

dict_Analysis = {}

for var_key, var_value in wano_file["TABS"]["Analysis"].items():
    dict_Analysis[var_key] = var_value    

dict_INCAR = check_IVDW(dict_INCAR)
dict_INCAR = check_SOC(dict_INCAR)

# Analysis in INCAR file
dict_INCAR = check_Bader(dict_Analysis, dict_INCAR)
dict_INCAR = check_DOS(dict_Analysis, dict_INCAR)
incar = Incar.from_dict(dict_INCAR)

incar.write_file('INCAR')

print("INCAR successfully created")