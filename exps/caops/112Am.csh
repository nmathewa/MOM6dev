#!/bin/csh -x
#PBS -N XXX
#PBS -j oe
#PBS -o XXX.log
#PBS -l walltime=4:00:00
#PBS -l select=4
#PBS -W umask=027
#PBS -A NRLSS03755018
#PBS -q standard
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
setenv Y01 "001"
C
C --- run in the tar directories.
C --- tarm: i.e. daily averaged files.
C
chmod 750 $S/tarm_${Y01}${A}
cd        $S/tarm_${Y01}${A}
#
/bin/rm *days* *.tar*
C
C --- tar into four files, 8 days each
C
/bin/rm -f               days*
ls -1 ${E}*.{a,b}     >! days
head -16 days         >! days1
comm -3  days   days1 >! days1x
head -16 days1x       >! days2
comm -3  days1x days2 >! days2x
head -16 days2x       >! days3
comm -3  days2x days3 >! days4
C
${APRUN} /bin/tar --format=posix --files-from=days1 -cvf ${E}_archm_${Y01}${A}1.tar >! ${E}_archm_${Y01}${A}1.tar.lis &
${APRUN} /bin/tar --format=posix --files-from=days2 -cvf ${E}_archm_${Y01}${A}2.tar >! ${E}_archm_${Y01}${A}2.tar.lis &
${APRUN} /bin/tar --format=posix --files-from=days3 -cvf ${E}_archm_${Y01}${A}3.tar >! ${E}_archm_${Y01}${A}3.tar.lis &
${APRUN} /bin/tar --format=posix --files-from=days4 -cvf ${E}_archm_${Y01}${A}4.tar >! ${E}_archm_${Y01}${A}4.tar.lis &
wait
C
${APRUN} /app/bin/pigz -p 8 --fast ${E}_archm_${Y01}${A}1.tar &
${APRUN} /app/bin/pigz -p 8 --fast ${E}_archm_${Y01}${A}2.tar &
${APRUN} /app/bin/pigz -p 8 --fast ${E}_archm_${Y01}${A}3.tar &
${APRUN} /app/bin/pigz -p 8 --fast ${E}_archm_${Y01}${A}4.tar &
#${APRUN} /usr/bin/gzip ${E}_archm_${Y01}${A}1.tar &
#${APRUN} /usr/bin/gzip ${E}_archm_${Y01}${A}2.tar &
#${APRUN} /usr/bin/gzip ${E}_archm_${Y01}${A}3.tar &
#${APRUN} /usr/bin/gzip ${E}_archm_${Y01}${A}4.tar &
wait
C
cd $S
awk -f $D/../${E}.awk y01=${Y01} ab=${A} $D/../${E}Am_rcp.csh >! tarm_${Y01}${A}_rcp.csh
~wallcraf/bin/q_navo tarm_${Y01}${A}_rcp.csh 
