![DFT-VASP WaNo logo](https://raw.githubusercontent.com/KIT-Workflows/DFT-VASP/main/DFT-VASP.png)

When publishing results obtained with DFT-VASP WaNo, please consider citing it. [![DOI](https://zenodo.org/badge/341835878.svg)](https://zenodo.org/badge/latestdoi/341835878)

# DFT-VASP
The DFT-VASP WaNo implements a wide range of methods available within the VASP code, one of the most widely used electronic structure programs. This WaNo allows experienced and inexperienced users to perform DFT calculations without requiring a deep understanding of VASP functionalities and specifications. The POSCAR file is the single mandatory file as the input of the WaNo. All the remaining VASP input files are automatically generated or loaded from an external source.

<button style="color:white; background-color:black; padding:10px 20px;">Click me!</button>


Figure 1 shows that this WaNo has the INCAR, KPOINTS, Analysis, and Files-Run tabs. The first one aims to define the INCAR file. This tab might be changed whenever the problem requires more input parameters, which is attained by adding the necessary flags in the XML file. The remaining tabs create the KPOINTS file and allow the user to perform DOS and Bader Charge Analysis, and the Files-Run controls the VASP compilation types (vasp_std, vasp_gam, and  vasp_ncl). It loads the POSCAR file and, as an option, may load INCAR, POTCAR, and KPOINTS too. 

![DFT-VASP WaNo GUI](https://raw.githubusercontent.com/KIT-Workflows/DFT-VASP/main/DFT-VASP_paramters.png)

**Fig 1** The DFT-VASP WaNo performs DFT calculation using Vasp code. In this WaNo, the POTCAR might be automatized after reading the POSCAR file. In the GUI, we can set the KPOINTS and INCAR files, but there is also the option to load the inputs file in the Files-Run tab.

## 1. Python Setup
To get this WaNo up and running on your available computational resources, make sure to have the below libraries installed on Python 3.6 or newer.

```
1. Atomic Simulation Environment (ASE).
2. Python Materials Genomics (Pymatgen).
3. Numpy, os, sys, re, yaml. 
```

## 2. DFT-VASP files and Inputs
- **INCAR tab**: See the GUI of this WaNo. as an option, we can set all INCAR flags available within VASP. However, we expose only a few of them, which are essential for the problem. A brief description of each flag pops up when we hover the mouse over the inputs.
- **KPOINTS tab**: Here the user can define two types of KPOINTS, `Kpoints_length` and `Kpoints_Monkhorst`.
- **Analysis tab**: Aimed to compute Bader charge analysis and DOS.
- **Files-Run tab**: Mandatory loads the POSCAR file, and as an option can load INCAR, POTCAR, KPOINTS, and KORINGA files. The KORINGA file can be any file. In the case of this problem, it loads the Input_data.yml file.
- **Properties tab**: This tab is optional but quite helpful to query properties from the OUTCAR file. Currently, any properties can be inquired using the get python functions in ASE (`get_total_energy, get_potential_energy, get_magnetic_moment`, and etc) or INCAR flags. In this tab, we must omit the term `get` and all the values of those properties or flags are saved in the dft_vasp_dict.yml dictionary file.
- All `.py` scripts may generate the INCAR, POTCAR, and KPOINTS files. 

## 3. DFT-VASP Output
- `OUTCAR`    
    - This file contains vital information about the simulation of the system.
- `CONTCAR`
    - The CONTCAR file contains information about the structure, e.g., the ionic positions.
- `POTCAR`
    - The POTCAR file essentially contains the pseudopotential for each atomic species used in the calculation.
- `vasp_results.yml`
    - This a dictionary file with some chosen information about the system. 

## 4. Running this Workflow

- Step 1. Move the DFT-VASP folder to the WaNo directory. 
- Step 2. Open Simstack on your compute and connect to your remote resource.
- Step 3. Drag the WaNo from the top left menu to the SimStack canvas as shown in **Fig 1**.
- Step 4. A double click on the WaNo will allow you to make the setups in the Input parameters.
- Step 5. Name your WaNo with `Ctrl+S`, and running it with `Ctrl+R` command.

## Acknowledgements
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 957189. The project is part of BATTERY 2030+, the large-scale European research initiative for inventing the sustainable batteries of the future.

## License & copyright
  Developer: Celso Ricardo C. Rêgo, 
  Multiscale Materials Modelling and Virtual Design,
  Institute of Nanotechnology, Karlsruhe Institute of Technology
  https://www.int.kit.edu/wenzel.php

Licensed under the [KIT License](LICENSE).
