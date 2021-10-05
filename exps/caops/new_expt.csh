#!/bin/csh
set echo
#
# --- build new expt files from old.
# --- some files will need additional manual editing.
#
#  O = old experiment number
#  N = new experiment number
#  R = region name.
#
setenv  O 111 
setenv  N 112
setenv  R GOMb0.08
#
setenv DO `echo ${O} | awk '{printf("expt_%04.1f", $1*0.1)}'`
setenv DN `echo ${N} | awk '{printf("expt_%04.1f", $1*0.1)}'`
#
setenv RO $R
setenv  D ../../${RO}/${DO}
#
foreach t ( .csh Am.csh Ar.csh Am_rcp.csh Ar_rcp.csh pbs.csh )
  sed -e "s/setenv E .*${O}.*/setenv E ${N}/g" -e "s/${DO}/${DN}/g"  -e "s/${RO}/${R}/g" ${D}/${O}${t} >! ${N}${t}
end
#
#foreach f ( cp_011a.csh )
#  sed -e "s/setenv E .*${O}.*/setenv E ${N}/g" -e "s/${DO}/${DN}/g"  -e "s/${RO}/${R}/g" ${D}/${f} >! ${f}
#end
#
cp ${D}/${O}.awk ${N}.awk
#
cp ${D}/MOM_input* ${D}/MOM_override* ${D}/MOM_layout* .
cp ${D}/SIS_input* ${D}/SIS_override* ${D}/SIS_layout* .
cp ${D}/dummy*.csh .
cp ${D}/*_table*   .
cp ${D}/*.nml*     .
cp ${D}/*.nc       .
#
# --- experiment run sequence:
#
mlist 115 115 1 a  
#cp  ${D}/LIST++ LIST
cp LIST LIST++
#
# --- create data directory (local and on archive):
#
mkdir data
#ssh newton.navo.hpc.mil mkdir -p /u/home/$user/MOM6/${R}/${DN}/data
#
# --- relax.ssh
#
#cd ../relax/SSH
#ln -s relax_ssh_010.a relax_ssh_${N}.a
#ln -s relax_ssh_010.b relax_ssh_${N}.b
