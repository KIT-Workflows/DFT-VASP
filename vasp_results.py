from ase.io.vasp import read_vasp_out
import yaml

def get_bandgap(location = "DOSCAR",tol = 1e-3):
    doscar = open(location)
    for i in range(6):
        l=doscar.readline()
    efermi = float(l.split()[3])
    step1 = doscar.readline().split()[0]
    step2 = doscar.readline().split()[0]
    step_size = float(step2)-float(step1)
    not_found = True
    while not_found:
        l = doscar.readline().split()
        e = float(l.pop(0))
        dens = 0
        for i in range(int(len(l)/2)):
            dens += float(l[i])
        if e < efermi and dens > tol:
            bot = e
        elif e > efermi and dens > tol:
            top = e
            not_found = False
    if top - bot < step_size*2:
        return 0,0,0
    else:
        #return top - bot,bot-efermi,top-efermi
        return top - bot,bot,top

def get_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append([line_number, line.rstrip()])
 
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

def find_line(filename, lookup, pos_vas):

    with open(filename) as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                t_num = num
                var_stg = line.split()[pos_vas]
    #print('found at line:', var_1, t_num)
    #print(var_stg)
    return var_stg

def find_by_key(data, target):
    for key, value in data.items():
        if isinstance(value, dict):
            yield from find_by_key(value, target)
        elif key == target:
            yield value

def call_find_by_key(data, target):

    y = []
    x = None
    
    for x in find_by_key(data, target):
        y.append(x) 
    
    return x

if __name__ == '__main__':

    with open('rendered_wano.yml') as file:
        wano_file = yaml.full_load(file)

    properties_bool = wano_file["TABS"]["Properties"]["properties"]
    import_inputs = wano_file["TABS"]["Properties"]["Import Inputs"]
    
    if properties_bool:
        a_dict = wano_file["TABS"]["Properties"]["Var-properties"]
        var_prop = wano_file["TABS"]["Properties"]["Var-properties"]
        a_key = list(a_dict[0].keys())[0]
        values_of_key = [a_dict[a_key] for a_dict in a_dict]

        file_outfile = "OUTCAR"
        atoms = read_vasp_out("OUTCAR")
        results_dict= {}

        #find_line(file_outfile, "NKPTS =", 3)
        results_dict["NKPTS"] = int(find_line(file_outfile, "NKPTS =", 3))
        results_dict["ENCUT"] = wano_file["TABS"]["INCAR"]["ENCUT"]

        for var in values_of_key:
            print(var)
            if var[0].isupper():
                cmd_1 = call_find_by_key(wano_file, var) #wano_file["TABS"]["INCAR"][var]
                results_dict[var] = cmd_1
            else:
                if var == "cell_lengths_and_angles":
                    cmd_1 = "atoms.get_{}{}".format(var, "()")
                    results_dict["a"] = float(eval(cmd_1)[0])
                    results_dict["c"] = float(eval(cmd_1)[2])
                    print(eval(cmd_1)[0],eval(cmd_1)[2])
                elif var == "label" or var == "title":
                    with open('rendered_wano.yml') as file:
                        wano_file = yaml.full_load(file)
                        
                    results_dict[var] = wano_file["TABS"]["Files-Run"]["Title"] 
                    # temp_var = (get_string_in_file("OUTCAR", "POSCAR")[1][1]).split()[2]
                    # results_dict[var] = temp_var
                elif var == "gap" or var == "Gap":
                    gap, vbm, cbm = get_bandgap()
                    results_dict["gap"] = gap
                    results_dict["vbm"] = vbm
                    results_dict["cbm"] = cbm
                else:
                    cmd_1 = "atoms.get_{}{}".format(var, "()")
                    results_dict[var] = eval(cmd_1)
                    print(results_dict)
    else:
        results_dict = {}
    
    if import_inputs:
        with open("Inputs.yml") as file:
            input_file = yaml.full_load(file)
        results_dict.update(input_file)

    with open("vasp_results.yml",'w') as out:
        yaml.dump(results_dict, out,default_flow_style=False)
    
    with open("output_dict.yml",'w') as out:
        yaml.dump(results_dict, out,default_flow_style=False)
    