import pymatgen
from pymatgen.io.vasp import Kpoints
from ast import literal_eval
import os, yaml

if __name__ == '__main__':

    if os.path.isfile('KPOINTS'):
        print("KPOINTS already loaded")
        exit
    else:
        with open('rendered_wano.yml') as file:
                wano_file = yaml.full_load(file)

        Rk = wano_file["TABS"]["KPOINTS"]["Kpoints_length"]
        Monkhorst = wano_file["TABS"]["KPOINTS"]["Kpoints_Monkhorst"]

        if  Rk:
            Rk_val = (wano_file["TABS"]["KPOINTS"]["Rk_length"])
            kpoints = Kpoints.automatic(Rk_val)
            kpoints.write_file('KPOINTS')
            print("KPOINTS successfully created")
        elif Monkhorst:
            mat_n = literal_eval(wano_file["TABS"]["KPOINTS"]["Monkhorst"])
            n = [mat_n[0][0], mat_n[0][1], mat_n[0][2]]
            n_shift = [mat_n[1][0], mat_n[1][1], mat_n[1][2]]
            kpoints = Kpoints.monkhorst_automatic(n, n_shift)
            # kpoints = Kpoints.gamma_automatic(n, n_shift)
            kpoints.write_file('KPOINTS')
            print("KPOINTS successfully created")
        else:
            None

        