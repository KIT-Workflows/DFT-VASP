#import pymatgen
from pymatgen.core import Structure, Lattice
from pymatgen.io.vasp import Incar, Poscar, Potcar, Kpoints 

from ase import io
from ase.io.vasp import read_vasp, write_vasp

#from pymatgen.io.vasp.sets import MPRelaxSet
import os, yaml

def get_VASP_inputs(structure):
    return dict(
        SYSTEM=structure.formula,  # Name of the system
        ## Electronic relaxation:
        ENCUT=500.0,  # 500. eV, value for carbon atom
        NELMIN=6,  # Minimum number of eletronic selfconsistency (SC) steps
        NELM=1000,  # Maximum number of electronic SC steps
        NELMDL=-12,  # Number of NON-selfconsistency steps
        EDIFF=1.0e-6,  # Global-break condition for the electronic SC-loop (ELM)
        ## Calculation mode:
        PREC='NORMAL',  # Calcululation level (Changes FFT-grids)
        ISPIN=2,  # spin-polarized calculations
        ADDGRID='.TRUE.',  # level of precision
        IVDW=0,  # no vdW corrections
        ## Ionic relaxation:
        NSW=150,  # Maximum number of ionic steps
        EDIFFG=-0.020,  # stop if all forces are smaller than |EDIFFG|
        IBRION=2,
        ISIF=3,  # Controls the computation of stress tensor. 3 computes everything
        POTIM=0.010,
        ## Integration over the Brillouin zone (BZ):
        ISMEAR=0,  # Gaussian smearing scheme. Use 0 for insulators, as suggested by VASPWIKI
        SIGMA=0.10,
        # LREAL   = 'Auto',        # Should projections be done in real space? Let VASP decide
        # ALGO   = 'ALL',
        ## DOS calculation:
        LORBIT=10,  # Calculate the DOS without providing the Wigner Seitz radius
        NEDOS=101,  # Number of points to calculate the DOS
        ## OUTCAR size:
        NWRITE=1,  # Determines how much information will be written in OUTCAR
        LCHARG='.FALSE.',  # Write charge densities?
        LWAVE='.FALSE.',  # write out the wavefunctions?
        LASPH='.TRUE.',  # non-spherical elements in the PAW method
        # NKRED = 8,
        ## Key for parallel mode calculation:
        NCORE=4,
        LPLANE='.TRUE.',  # Plane distribution of FFT coefficients. Reduces communications in FFT.
    )

def check_IVDW(dict_INCAR):
    var_value = dict_INCAR.get("IVDW")
    ivdw_data = {"D2": 10, "D3": 11, "D3BJ": 12, "dDsC": 4, "TSSCS": 20, "TSHP": 21, "MBDSC": 202, "MBDFI": 263, "None": 0}
    dict_INCAR['IVDW'] = ivdw_data[var_value]
    dict_INCAR['ADDGRID'] = '.FALSE.'
    dict_INCAR['LASPH'] = '.FALSE.'
    
    return dict_INCAR

def check_vdw_functional(dict_INCAR):
    var_value = dict_INCAR.get('GGA')
    if var_value == "optPBE-vdw":
        dict_INCAR['GGA'] = "OR"
        dict_INCAR['LUSE_VDW'] = ".TRUE."
        dict_INCAR['AGGAC'] = 0.0000
        dict_INCAR['LASPH'] = ".TRUE."
    elif var_value == "optB88-vdw":
        dict_INCAR['GGA'] = "BO"
        dict_INCAR['PARAM1'] = 0.1833333333
        dict_INCAR['PARAM2'] = 0.2200000000
        dict_INCAR['LUSE_VDW'] = ".TRUE."
        dict_INCAR['AGGAC'] = 0.0000
        dict_INCAR['LASPH'] = ".TRUE."
    elif var_value == "optB86b-vdw":
        dict_INCAR['GGA'] = "MK"
        dict_INCAR['PARAM1'] = 0.1234 
        dict_INCAR['PARAM2'] = 1.0000
        dict_INCAR['LUSE_VDW'] = ".TRUE."
        dict_INCAR['AGGAC'] = 0.0000
        dict_INCAR['LASPH'] = ".TRUE."
    elif var_value == "SCAN+rVV10":
        dict_INCAR['METAGGA']  = "SCAN"
        dict_INCAR['LUSE_VDW'] = ".TRUE."
        dict_INCAR['BPARAM'] = 6.3     # default but can be overwritten by this tag
        dict_INCAR['CPARAM'] = 0.0093  # default but can be overwritten by this tag
        dict_INCAR['LASPH'] = ".TRUE."
        del dict_INCAR["GGA"]
    else:
        dict_INCAR['GGA'] = var_value
        dict_INCAR = check_IVDW(dict_INCAR)
    return dict_INCAR

def check_hybrid_functionals(dict_INCAR):
    var_value = dict_INCAR.get('GGA')
    if var_value == 'HSE03':
        _extracted_from_check_hybrid_functionals_4("PE", dict_INCAR, ".TRUE.", 0.3000)
    elif var_value == 'HSE06':
        _extracted_from_check_hybrid_functionals_4('PE', dict_INCAR, '.TRUE.', 0.2000)
    else:
        dict_INCAR['GGA'] = var_value

    return dict_INCAR


# TODO Rename this here and in `check_hybrid_functionals`
def _extracted_from_check_hybrid_functionals_4(arg0, dict_INCAR, arg2, arg3):
    dict_INCAR['GGA'] = arg0
    dict_INCAR['LHFCALC'] = arg2
    dict_INCAR['HFSCREEN'] = arg3

def check_SOC(dict_INCAR):
    if "SOC" in dict_INCAR.keys() and dict_INCAR["SOC"] == True:
        dict_INCAR["LASPH"] = ".TRUE."
        dict_INCAR["LSORBIT"] = ".TRUE."
        dict_INCAR["GGA_COMPAT"] = ".TRUE."
        dict_INCAR["SAXIS"] = "0 0 1"    
        dict_INCAR["ISYM"] = 0
    
    del dict_INCAR["SOC"]
    return dict_INCAR

def check_MD(dict_INCAR):
    if "MD" in dict_INCAR.keys() and dict_INCAR["MD"] == True:
        dict_INCAR["ISYM"] = 0
        dict_INCAR["IBRION"] = 0
        dict_INCAR["ISMEAR"] = 0
        dict_INCAR["ALGO"] = "Very Fast"
        dict_INCAR["LWAVE"] = ".FALSE."
        dict_INCAR["LCHARG"] = ".FALSE."

        if dict_INCAR["CPMD"]["Ensemble"] == "NVE":
            dict_INCAR["MDALGO"] = 1
            dict_INCAR["ANDERSEN_PROB"] = 0.0
            dict_INCAR["ISIF"] = 2
            dict_INCAR["SMASS"] = -3 # Nose-Hoover thermostat
        else:
            dict_INCAR["MDALGO"] = 2
            dict_INCAR["ISIF"] = 2
            dict_INCAR["SMASS"] = 0

        dict_INCAR["SMASS"] = -3 # Nose Hoover thermostat
        dict_INCAR["TEBEG"] = dict_INCAR["CPMD"]["TEBEG"] # Init temperature 
        dict_INCAR["TEEND"] = dict_INCAR["CPMD"]["TEEND"] # End temperature

        print(dict_INCAR["CPMD"]["Ensemble"])
    del dict_INCAR["MD"]
    del dict_INCAR["CPMD"]
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
        dict_INCAR["LORBIT"]  = dict_Analysis["dos_calculation"].get("LORBIT")
        dict_INCAR["NSW"]  = dict_Analysis["dos_calculation"].get("NSW")
        #dict_INCAR["ISMEAR"]  = dict_Analysis["dos_calculation"].get("ISMEAR")
        dict_INCAR["PREC"]  = dict_Analysis["dos_calculation"].get("PREC")
    return dict_INCAR

def check_Band_structure(dict_Analysis, dict_INCAR):
    if "Band_Structure" in dict_Analysis.keys() and dict_Analysis["Band_Structure"] == True:  
        dict_INCAR["IBRION"]  = dict_Analysis["band"].get("IBRION")
        dict_INCAR["ICHARG"]  = dict_Analysis["band"].get("ICHARG")
        dict_INCAR["LORBIT"]  = dict_Analysis["band"].get("LORBIT")
        dict_INCAR["NSW"]  = dict_Analysis["band"].get("NSW")
        dict_INCAR["PREC"]  = dict_Analysis["band"].get("PREC")
        
    return dict_INCAR

if __name__ == '__main__':

    with open('rendered_wano.yml') as file:
        wano_file = yaml.full_load(file)
##############################################################################

    label_var = wano_file["TABS"]["Files-Run"]["Title"]

    structure = io.read("POSCAR")
    write_vasp('POSCAR', structure, label=None, direct=True, vasp5=True, long_format=True)

    # Create bash file
    file_name = "run_vasp.sh"
    with open(file_name, 'w') as f:
        f.write('#!/bin/bash\n')
        f.write('. /etc/profile.d/lmod.sh\n')
        f.write('set -e\n')

        f.write('module purge\n')
        vasp_v = wano_file["TABS"]["Files-Run"]["vasp version"]
        f.write(f'module load vasp/{vasp_v} prun\n')
        
        f.write('\n')

        if wano_file["TABS"]["INCAR"]["SOC"]:
            f.write('prun vasp_ncl\n')
        else: 
            f.write('prun ' + wano_file["TABS"]["Files-Run"]["prun_vasp"])

    os.system(f"chmod +x {file_name}")

    if os.path.isfile('INCAR'):
        print("INCAR already loaded")
        exit
    else:
        structure = Structure.from_file("POSCAR")   
        dict_INCAR = get_VASP_inputs(structure)

        # Reading the inputs for INCAR file
        for var_key, var_value in wano_file["TABS"]["INCAR"].items():
            if var_key in dict_INCAR.keys():
                dict_INCAR[var_key] = var_value
                print(var_key, var_value)
            else:
                dict_INCAR[var_key] = var_value

        dict_Analysis = {}

        for var_key, var_value in wano_file["TABS"]["Analysis"].items():
            if var_key == 'ENCUT':
                var_value = float(var_value)

            dict_Analysis[var_key] = var_value     

        dict_INCAR = check_vdw_functional(dict_INCAR)
        dict_INCAR = check_hybrid_functionals(dict_INCAR)
        dict_INCAR = check_SOC(dict_INCAR)
        dict_INCAR = check_MD(dict_INCAR)

        # Analysis in INCAR file
        dict_INCAR = check_Bader(dict_Analysis, dict_INCAR)
        dict_INCAR = check_DOS(dict_Analysis, dict_INCAR)
        dict_INCAR = check_Band_structure(dict_Analysis, dict_INCAR)
        incar = Incar.from_dict(dict_INCAR)

        incar.write_file('INCAR')
        print("INCAR successfully created")