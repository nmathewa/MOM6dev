#!/bin/csh -x
#PBS -N XXX
#PBS -j oe
#PBS -o XXX.log
#PBS -l walltime=3:00:00
#PBS -l select=1
#PBS -W umask=027
#PBS -A NRLSS03755018
#PBS -q standard
#
set echo
set time = 1
set timestamp
date +"Start       %c"
C
C --- tar restart files in a batch job
C
setenv OS `uname`
setenv APRUN    ""
C
C --- pget, pput "copy" files between scratch and permanent storage.
C --- Can both be cp if the permanent filesystem is mounted locally.
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
switch ($OS)
case 'SunOS':
case 'Linux':
case 'AIX':
case 'XT4':
    if (-e ~wallcraf/bin/pget) then
      setenv pget ~wallcraf/bin/pget
      setenv pput ~wallcraf/bin/pput
    else
      setenv pget /bin/cp
      setenv pput /bin/cp
    endif
    breaksw
default:
    setenv pget /bin/cp
    setenv pput /bin/cp
endsw
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
case 'HP-UX':
    setenv S     /scratch3/${user}/$P
    breaksw
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
case 'IRIX64':
    setenv S     /scr/${user}/$P
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
      setenv D     /p/home/${user}/$P
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
setenv B " "
setenv Y01 "001"
setenv YXX "001"
C
C --- run in the scratch directory.
C
cd $S
#
C
C --- tar into one big file
C
/bin/rm -f                            RESTART_${YXX}${B}.tar
${APRUN} /bin/tar --format=posix -cvf RESTART_${YXX}${B}.tar RESTART_${YXX}${B} >! RESTART_${YXX}${B}.tar.lis
date +"After tar   %c"
#${APRUN} /usr/bin/gzip                RESTART_${YXX}${B}.tar
${APRUN} /app/bin/pigz -p 8 --fast    RESTART_${YXX}${B}.tar
date +"After pigz  %c"
C
awk -f $D/../${E}.awk y01=${Y01} ab=${A} $D/../${E}Ar_rcp.csh >! RESTART_${YXX}${B}_rcp.csh
~wallcraf/bin/q_navo RESTART_${YXX}${B}_rcp.csh
