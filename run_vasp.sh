#!/bin/bash
. /etc/profile.d/lmod.sh
set -e
module purge
module load vasp prun
{% if wano["TABS"]["Files_Run"]["SOC"] -%}
{{ "prun vasp_ncl"  }}
{% else %}
{{ "prun" }} {{ wano["TABS"]["Files_Run"]["prun_vasp"] }}
{%- endif %}
