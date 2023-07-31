from ase.io.vasp import read_vasp_out, read_vasp
import ase.io.vasp
import yaml, re, sqlite3, datetime, json, array
from ase.cell import Cell
import numpy as np

class Util_tricks:

    def find_last_line(self, filename, string):

        with open(filename, 'r') as file:
            lines = file.readlines()
            last_line = None
            for line in lines:
                if string in line:
                    last_line = line
            return last_line
    
    def metadata(self, dict_properties):

        self.dict_properties = dict_properties

        results_dict['user'] = 'Your user name'

        current_datetime = datetime.datetime.now()
        self.dict_properties['datetime'] = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        return dict_properties

class Vasp_properties:
    
    def __init__(self, properties_bool, dict_properties):
        self.properties_bool = properties_bool
        self.dict_properties = dict_properties 

    def check_conv_vasp(self):

        '''
        Check if the convergency criteria was reached in the last iteration        
        '''

        with open('OUTCAR', 'r') as f:
            outcar_lines = f.readlines()

        # Find the last iteration of the electronic minimization loop
        for i, line in enumerate(reversed(outcar_lines)):
            if "reached required accuracy" in line:
                break

        # Check if the convergency criteria was reached in the last iteration

        if "reached required accuracy" in outcar_lines[-i-1]:
            
            print("VASP calculations successfully finished")

            self.dict_properties["convergence"] = "Yes"
        else:
            
            print("VASP calculations not successfully finished")
            self.dict_properties["convergence"] = "No"

        return self.dict_properties

    def get_bandgap(self, location = "DOSCAR",tol = 1e-3):
        doscar = open(location)
        for _ in range(6):
            l=doscar.readline()
        efermi = float(l.split()[3])
        step1 = doscar.readline().split()[0]
        step2 = doscar.readline().split()[0]
        step_size = float(step2)-float(step1)
        not_found = True
        while not_found:
            l = doscar.readline().split()
            e = float(l.pop(0))
            dens = sum(float(l[i]) for i in range(len(l) // 2))
            if e < efermi and dens > tol:
                bot = e
            elif e > efermi and dens > tol:
                top = e
                not_found = False
        if top - bot < step_size*2:

            self.dict_properties["band_gap"] = 0.0
            self.dict_properties["vbm"] = 0.0
            self.dict_properties["cbm"] = 0.0

        else:
            self.dict_properties["band_gap"] = top - bot
            self.dict_properties["vbm"] = bot-efermi
            self.dict_properties["cbm"] = top-efermi


        return self.dict_properties

    def get_pressures(self):

        ''' This function will return the external pressure and Pullay stress in kB '''

        ut = Util_tricks() 
        press = ut.find_last_line('OUTCAR', 'pressure')
        press =press.split("kB")
        self.dict_properties["external_pressure"] = float(re.findall(r'[+-]?\d+.\d+', press[0])[0])
        self.dict_properties["pullay_stress"] = float(re.findall(r'[+-]?\d+.\d+', press[1])[0])

        return self.dict_properties

    def get_vasp_properties(self):
        ''' Pressure and band gap aren't supported in ASE '''
        try:
            self.check_conv_vasp()
            self.get_pressures()
            self.get_bandgap()
        except IndexError:
            print("The calculation did not converge")

        ''' Supported properties in ASE '''
        atoms = read_vasp_out("OUTCAR") # read inside eval 
        a = "atoms.get_"
        c = "()"

        for var_prop in self.properties_bool:
            property_value = eval("".join([a, var_prop, c]))

            if isinstance(property_value, (np.ndarray, Cell)):
                self.dict_properties[var_prop] = property_value.tolist()
            elif isinstance(property_value, np.float64):
                self.dict_properties[var_prop] = float(property_value)
            else:
                self.dict_properties[var_prop] = property_value

        return self.dict_properties


if __name__ == '__main__':

    with open('rendered_wano.yml') as file:
        wano_file = yaml.full_load(file)

    results_dict = {}

    if wano_file["TABS"]["Files-Run"]["vasp version"] == "5.4.4":
        ''' current_datetime '''

        ut = Util_tricks()
        ut.metadata(results_dict)


        ''' Supported properties in ASE '''

        properties_bool = ['total_energy', 'potential_energy', 'kinetic_energy', 'cell',  
                        'cell_lengths_and_angles', 'positions', 'forces', 
                'chemical_formula', 'chemical_symbols', 'center_of_mass', 'volume', 'temperature', 'all_distances', 
                'masses', 'atomic_numbers', 'global_number_of_atoms', 'initial_charges']

        if wano_file['TABS']['INCAR']['ISPIN'] == 2:
            properties_bool.extend(('magnetic_moment', 'magnetic_moments'))

        properties_vasp = Vasp_properties(properties_bool, results_dict)

        results_dict = properties_vasp.get_vasp_properties()


    ''' Pressure and band gap aren't supported in ASE '''
    wano_file = {**wano_file, **results_dict}

    with open("vasp_results.yml", "w") as out:
        yaml.dump(wano_file, out, default_flow_style=False)
    
    # with open("db_vasp_results.yml", "w") as out:
    #     yaml.dump(wano_file, out, default_flow_style=False)
    
