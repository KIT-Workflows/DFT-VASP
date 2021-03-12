# DFT-VASP
The DFT-VASP WaNo implements a wide range of methods available within the VASP code, one of the most widely used electronic structure programs. This WaNo affords experienced and inexperienced users to perform DFT calculations without requiring a deep understanding of VASP functionalities and specifications. The POSCAR file is the single mandatory file as the input of the WaNo. All the remaining VASP input files are automatically generated.

Figure 1 shows that this WaNo has the INCAR, KPOINTS, Analysis, and Files_Run tabs. The first one aims to define the INCAR file. This tab might be changed whenever the problem requires more input parameters, which is attained by adding the necessary flags in the XML file. The remaining tabs create the KPOINTS file, allows the user to perform DOS and Bader Charge Analysis, and the Files_Run controls the VASP compilation types (vasp_std, vasp_gam, and  vasp_ncl). It loads the POSCAR file and, as an option, may load INCAR, POTCAR, KPOINTS too. 

![Semantic description of image](parameters-DFT-VASP.png)

**Fig 1** The DFT_VASP WaNo performs DFT calculation using Vasp code. In this WaNo, the POTCAR might be automatized after reading the POSCAR file. In the GUI, we can set the KPOINTS and INCAR files, but there is also the option to load the inputs file in the Files_Run tab.

## 1. Python Setup
To get this WaNo up running on your available computational resources, make sure to have the below libraries installed on Python 3.6 or newer.

```
1. Atomic Simulation Environment (ASE).
2. Python Materials Genomics (Pymatgen).
3. Numpy, os, sys, re, yaml. 
```

## 1. DFT-VASP files and Inputs
- **INCAR tab**: as an option, we can set all INCAR flags available within VASP. However, we expose only a few of them, which are essential for the problem. See the GUI of this WaNo. A brief description of each flag pops up when we rover the mouse over the inputs.
- **KPOINTS tab**: Here the user can define two types of KPOINTS, `Kpoints_length` and `Kpoints_Monkhorst`.
- **Analysis tab**: Aimed to compute Bader charge analysis and DOS.
- **Files_Run tab**: Mandatory loads the POSCAR file, and as an option can load INCAR, POTCAR, KPOINTS, and KORINGA files. The KORINGA file can be any file. In the case of this problem, it loads the Input_data.yml file.
- All `.py` scripts may generate the INCAR, POTCAR, and KPOINTS files. 
## 2. DFT-VASP Output
- OUTCAR    
    - This file must return the properties of the system.

## Running this Workflow

- Step 1. Move the DFT-VASP folder to the WaNo directory. 
- Step 2. Open Simstack on your compute and connect to your remote resource.
- Step 3. Drag the WaNo from the top left menu to the SimStack canvas as shown in **Fig 1**.
- Step 4. A double click on the WaNo will allow you to make the setups in the Input parameters.
- Step 5. Name your WaNo with `Ctrl+S`, and running it with `Ctrl+R` command.
