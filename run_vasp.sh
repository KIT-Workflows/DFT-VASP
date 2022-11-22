#!/bin/bash
. /etc/profile.d/lmod.sh
set -e
module purge
module load vasp prun

prun vasp_std