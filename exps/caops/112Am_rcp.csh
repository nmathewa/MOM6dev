#!/bin/csh -x
#PBS -N XXX
#PBS -j oe
#PBS -o XXX.log
#PBS -l walltime=12:00:00
#PBS -l select=1
#PBS -A NRLSS03755018
#PBS -q transfer
#
set echo
set time = 1
set timestamp
C
C --- tar archive files in a batch job
C
setenv OS `uname`
setenv APRUN    ""
C
switch ($OS)
case 'SunOS':
C   assumes /usr/5bin is before /bin and /usr/bin in PATH.
    breaksw
case 'Linux':
    which aprun
    if (! $status) then
C --- XT4, XT5 or XC30
      setenv OS XT4
      setenv APRUN      "aprun -n 1"
    endif
    breaksw
case 'OSF1':
    breaksw
case 'IRIX64':
    breaksw
case 'AIX':
    breaksw
default:
    echo 'Unknown Operating System: ' $OS
    exit (1)
endsw
C
C --- copy files between scratch and permanent storage.
C
C --- E is expt number.
C --- P is primary path.
C --- D is permanent directory.
C --- S is scratch   directory, must not be the permanent directory.
C
setenv E 029
setenv X `echo ${E} | awk '{printf("%04.1f", $1*0.1)}'`
setenv R GOMb0.08
setenv P MOM6/${R}/expt_${X}/data
setenv D ~/$P
C
switch ($OS)
case 'OSF1':
#                ASC MSRC
    setenv S     /workspace/${user}/$P
    breaksw
case 'SunOS':
    if (-e /net/hermes/scrb) then
#                  NRLSSC
      setenv S     /net/hermes/scrb/${user}/$P
    else
#                  NAVO MSRC
      setenv S     /scr/${user}/$P
    endif
    breaksw
case 'AIX':
case 'Linux':
case 'XT4':
    if      (-e /gpfs/work) then
#                  ERDC MSRC
      setenv S     /gpfs/work/${user}/$P
    else if (-e /scr) then
#                  NAVO MSRC
      setenv D     /u/home/${user}/$P
      setenv S        /scr/${user}/$P
    else if (-e /p/work1) then
#                  NAVO MSRC
      setenv D     /u/home/${user}/$P
      setenv S    /p/work1/${user}/$P
    else if (-e /scratch/tempest) then
#                  MHPCC DC
      setenv S     /scratch/tempest/users/${user}/$P
    else if (-e /work) then
#                  ERDC
      setenv S     /work/${user}/$P
    else
#                  ARL MSRC
      setenv S     /usr/var/tmp/${user}/$P
    endif
    breaksw
endsw
C
setenv A " "
setenv Y01 "001"
C
C --- run in the tar directories.
C --- tarm: i.e. daily averaged HYCOM files.
C
cd $S/tarm_${Y01}${A}
C
${APRUN} /usr/bin/rcp ${E}_archm_${Y01}${A}1.tar.gz newton:${D} &
${APRUN} /usr/bin/rcp ${E}_archm_${Y01}${A}2.tar.gz newton:${D} &
${APRUN} /usr/bin/rcp ${E}_archm_${Y01}${A}3.tar.gz newton:${D} &
${APRUN} /usr/bin/rcp ${E}_archm_${Y01}${A}4.tar.gz newton:${D} &
wait
