#! /bin/csh
#
# --- check that the C comment command is available.
#
C >& /dev/null
if (! $status) then
  if (-e ${home}/hycom/ALL/bin/C) then
    set path = ( ${path} ${home}/hycom/ALL/bin )
  else
    echo "Please put the command hycom/ALL/bin/C in your path"
  endif
endif
C
set echo
set time = 1
set timestamp
date +"START  %c"
C
C --- MOM6 Experiment GOMb0.08 - 01.X series
C --- 41 layer sig2star MOM6+SIS2_symmetric for Gulf of Mexico region.
C --- 11.2 - start from TS of HYCOM GOFS3.1 2015-01-01-09
C ---        sponge T,S,U,v from HYCOM GOFS3.1 
C ---        OBC T,S,U,V Flather,Orlanski HYCOM GOFS3.1
C ---        CFSv2 atmos forcing - absolute wind

C --- Preamble, script keys on O/S name.
C
C --- Set parallel configuration, see ../README/README.expt_parallel.
C --- NOMP = number of OpenMP threads, 0 for no OpenMP, 1 for inactive OpenMP
C --- NMPI = number of MPI    tasks,   0 for no MPI
C
setenv APRUN1 ""
C
setenv OS `uname`
switch ($OS)
case 'Linux':
    if ($?XTPE_NETWORK_TARGET) then
      if ($XTPE_NETWORK_TARGET == "aries") then
#       setenv OS XC30
        setenv OS XC40
      endif
      setenv APRUN1 "aprun -n 1"
    endif
    which dplace
    if (! $status) then
      setenv OS HPE
      unset echo
      module purge
#     module load compiler/intel/2018.1.163
#     module load compiler/intel/2017.4.196
      module load compiler/intel/2019.4.243
      module load mpt/2.17
      module load costinit
      module load netcdf-c/intel/4.3.3.1
      module load netcdf-fortran/intel/4.4.2
      module load hdf5/intel/1.8.15
      module list
      set echo
    endif
    which poe
    if (! $status) then
      setenv OS IDP
      module swap mpi mpi/intel/impi/4.1.0
      module load mkl
      module list
    endif
    breaksw
endsw
switch ($OS)
case 'Linux':
case 'IDP':
    setenv NOMP 0
    setenv NMPI 64
    breaksw
case 'HPE':      
    setenv NOMP 0
    setenv NMPI 48
    breaksw
case 'XC30':
case 'XC40':
    setenv NOMP 0
    setenv NMPI 64
    breaksw
case 'AIX':
    setenv NOMP 0
    setenv NMPI 64
    breaksw
default:
    echo 'Unknown Operating System: ' $OS
    exit (1)
endsw
echo "NOMP is " $NOMP " and NMPI is " $NMPI
C
C --- R is region name.
C --- V is source code location
C --- T is topography number.
C --- K is number of layers.
C --- E is expt number.
C --- P is primary path.
C --- D is permanent directory.
C --- S is scratch   directory, must not be the permanent directory.
C
setenv R GOMb0.08
setenv V ~/MOM6-examples_FMS/build/intel
setenv T 09m11
setenv K 41
setenv E 112
setenv P HYCOM3-examples/${R}/expt_11.2/data
setenv D ~/$P
C
switch ($OS)
case 'Linux':
case 'IDP':
    if (-e /export/a/$user) then
#              NRLSSC
      setenv S /export/a/${user}/$P
    else if (-e /scr) then
#                  NAVO MSRC
      mkdir        /scr/${user}
      chmod a+rx   /scr/${user}
      setenv S     /scr/${user}/$P
    else
#              Single Disk
      setenv S ~/$P/SCRATCH
    endif
    breaksw
case 'HPE':      
    if      (-e /p/work1) then
#                  Navy MSRC
      mkdir        /p/work1/${user}
      chmod a+rx   /p/work1/${user}
      setenv S     /p/work1/${user}/$P
    else
#                  Single Disk
      setenv S     ~/$P/SCRATCH
    endif
    mkdir -p         $S
    lfs setstripe    $S -S 1048576 -i -1 -c 8
    breaksw
case 'XC30':
    if      (-e /p/work1) then
#                  Navy MSRC XC30
      mkdir        /p/work1/${user}
      chmod a+rx   /p/work1/${user}
      setenv S     /p/work1/${user}/$P
    else
#                  Single Disk
      setenv S     ~/$P/SCRATCH
    endif
    mkdir -p         $S
#   lfs setstripe    $S -S 1048576 -i -1 -c 24
    lfs setstripe    $S -S 1048576 -i -1 -c 8
    breaksw
case 'XC40':
    if      (-e /p/work1) then
#                  Navy MSRC XC40
      mkdir        /p/work1/${user}
      chmod a+rx   /p/work1/${user}
      setenv S     /p/work1/${user}/$P
    else
#                  Single Disk
      setenv S     ~/$P/SCRATCH
    endif
    mkdir -p         $S
    lfs setstripe    $S -S 1048576 -i -1 -c 8
#   lfs setstripe    $S -S 1048576 -i -1 -c 24
#   lfs setstripe    $S -S 1048576 -i -1 -c 48
    breaksw
case 'AIX':
    if      (-e /gpfs/work) then
#                  ERDC MSRC, under PBS
      mkdir        /gpfs/work/${user}
      chmod a+rx   /gpfs/work/${user}
      setenv S     /gpfs/work/${user}/$P
      setenv POE  pbspoe
    else if (-e /scr) then
#                  NAVO MSRC, under LoadLeveler or LSF
      mkdir        /scr/${user}
      chmod a+rx   /scr/${user}
      setenv S     /scr/${user}/$P
      if ($?LSB_JOBINDEX) then
        setenv POE mpirun.lsf
      else
        setenv POE poe
      endif
    else
#                  ARL MSRC, under GRD
      mkdir        /usr/var/tmp/${user}
      chmod a+rx   /usr/var/tmp/${user}
      setenv S     /usr/var/tmp/${user}/$P
      setenv POE  grd_poe
    endif
    breaksw
endsw
C
mkdir -p $S
cd       $S
C
C --- For whole year runs.
C ---   Y01 initial model year of this run.
C ---   YXX is the last model year of this run, and the first of the next run.
C ---   A and B are identical, typically blank.
C --- For part year runs.
C ---   A is this part of the year, B is next part of the year.
C ---   Y01 is the start model year of this run.
C ---   YXX is the end   model year of this run, usually Y01.
C --- For a few hour/day run
C ---   A   is the start day and hour, of form "dDDDhHH".
C ---   B   is the end   day and hour, of form "dXXXhYY".
C ---   Y01 is the start model year of this run.
C ---   YXX is the end   model year of this run, usually Y01.
C --- Note that these variables are set by the .awk generating script.
C
setenv A "a"
setenv B "b"
setenv Y01 "018"
setenv YXX "018"
setenv YOF `echo ${Y01} | awk '{printf("%04.0f", $1+1900)}'`
C
echo "Y01 =" $Y01 "YXX = " $YXX  "A =" ${A} "B =" ${B}
C
C --- local input files.
C
foreach f ( MOM_input MOM_override SIS_input SIS_override diag_table field_table )
  /bin/rm -f        ${f}
  if (-e    ${D}/../${f}_${Y01}${A}) then
    /bin/cp ${D}/../${f}_${Y01}${A} ${f}
  else
    /bin/cp ${D}/../${f}            ${f}
  endif
end
foreach f ( data_table )
  /bin/rm -f        ${f}
  if (-e    ${D}/../${f}_${Y01}) then
    /bin/cp ${D}/../${f}_${Y01} ${f}
  else
    /bin/cp ${D}/../${f}        ${f}
  endif
end
C
if ($NMPI != 0) then
  setenv NMPI4 `echo $NMPI | awk '{printf("%04d", $1)}'`
  foreach f ( MOM_layout SIS_layout )
    /bin/rm -f      ${f}
    /bin/cp ${D}/../${f}_${NMPI4} ${f}
  end
endif
C
if (-e    ${D}/../${E}y${Y01}${A}.limits) then
  /bin/cp ${D}/../${E}y${Y01}${A}.limits limits
else
#  use "LIMITI"  when starting a run after day zero.
#  use "LIMITS9" (say) for a 9-day run
  echo "LIMITS" | awk -f ${D}/../${E}.awk y01=${Y01} ab=${A} >! limits
endif
cat limits
setenv DI `cat limits | awk '{printf("%d\n",$2-$1)}'`
setenv DF `cat limits | awk '{printf("%15.2f\n", $1)}' limits`
setenv YF `echo $DF 3 | hycom_wind_ymdh | sed -e "s/_/,/g" -e 's/$/,00,00/g'`
C
if (-e ${D}/../input.nml_${Y01}${A}) then
  sed -e "s/NMPI/${NMPI}/g" -e "s/YYYA/${Y01}${A}/g" -e "s/YYYB/${YXX}${B}/g" -e "s/YYYY,MM,DD,HH,MM,SS/${YF}/g" -e "s/DD/${DI}/g" ${D}/../input.nml_${Y01}${A} >! input.nml
else
  sed -e "s/NMPI/${NMPI}/g" -e "s/YYYA/${Y01}${A}/g" -e "s/YYYB/${YXX}${B}/g" -e "s/YYYY,MM,DD,HH,MM,SS/${YF}/g" -e "s/DD/${DI}/g" ${D}/../input.nml >! input.nml
endif
C
C --- pget, pput "copy" files between scratch and permanent storage.
C --- Can both be cp if the permanent filesystem is mounted locally.
C
switch ($OS)
case 'AIX':
#case 'Linux':
    if      (-e ~wallcraf/bin/pget_navo) then
      setenv pget ~wallcraf/bin/pget_navo
      setenv pput ~wallcraf/bin/pput_navo
    else if (-e ~wallcraf/bin/pget) then
      setenv pget ~wallcraf/bin/pget
      setenv pput ~wallcraf/bin/pput
    else
      setenv pget /bin/cp
      setenv pput /bin/cp
    endif
    breaksw
case 'IDP':
case 'XC30':
case 'XC40':
#   setenv pget /bin/cp
    setenv pget ~wallcraf/bin/pget
    setenv pput ~wallcraf/bin/pput
    breaksw
default:
    setenv pget /bin/cp
    setenv pput /bin/cp
endsw
C
C --- input files mostly from file server.
C
mkdir -p INPUT
cd       INPUT
C
/bin/rm -f      mom6_vgrid.nc
/bin/cp ${D}/../mom6_vgrid.nc mom6_vgrid.nc
C
C --- for this region
C

C
C --- OBC
C
 /bin/cp ${S}/../../datasets/OBC_DAILY/obc_GOMb0.08_*_${YOF}*_53X_daily.nc .
 /bin/rm obc_south.nc
 /bin/rm obc_east.nc
 /bin/rm obc_north.nc
 
 ln -s obc_GOMb0.08_south_${YOF}${A}_53X_daily.nc obc_south.nc
 ln -s obc_GOMb0.08_east_${YOF}${A}_53X_daily.nc obc_east.nc
 ln -s obc_GOMb0.08_north_${YOF}${A}_53X_daily.nc obc_north.nc

#setenv ERMU ""
setenv ERMU 151
setenv ETSE 031
if ($ERMU != "") then
  foreach f ( Sponge_rmu_${ERMU}.nc ${ETSE}_Sponge_TSe_${Y01}${A}.nc )
    touch  $f
    if (-z $f) then
      ${pget} ${S}/../../datasets/$f $f &
    endif
  end
  ln -sf Sponge_rmu_${ERMU}.nc            Sponge_rmu.nc
#  ln -sf IC_rmu_4h_gomb08.nc              Sponge_rmu.nc
  ln -sf ${ETSE}_Sponge_TSe_${Y01}${A}.nc Sponge_TSe.nc
endif
#
foreach f ( atmos_mosaic_tile1Xland_mosaic_tile1.nc atmos_mosaic_tile1Xocean_mosaic_tile1.nc chl_mom6.nc depth_${R}_${T}_mom6.nc grid_spec.nc land_mask.nc land_mosaic_tile1Xocean_mosaic_tile1.nc ocean_mask.nc ocean_mosaic.nc regional.mom6.nc sss_mom6.nc rivers_${T}_mom6.nc )
  touch  $f
  if (-z $f) then
    ${pget} ${S}/../../datasets/$f $f &
  endif
end
setenv MSK `grep "MASKTABLE" ../MOM_layout | sed -e 's/^.*mask_/mask_/' -e 's/".*$//'`
if ($MSK != "") then
  /bin/cp ${S}/../../topo/partit/$T/$MSK $MSK
endif
C
C --- From obs
C
#foreach f ( GDEM42-40z_pottemp_salt.nc analysis_vgrid_lev35.v1.nc )
foreach f (53X_archm.${YOF}${A}_sponge_mask0t.nc)
  touch  $f
  if (-z $f) then
    ${pget} ${S}/../../datasets/$f $f &
  endif
end
\rm 53X_archm.sponge_mask.nc

C --- Sponge files
ln -s 53X_archm.${YOF}${A}_sponge_mask0t.nc 53X_archm.sponge_mask.nc

C --- Initial Conditions
foreach f ( 53X_archm.2015010109_tsuv_filled.nc )
  touch  $f
  if (-z $f) then
    ${pget} ${S}/../../datasets/INITIAL_CONDITIONS/$f $f &
  endif
end

C
C --- DA incremental update
C 
cp ${S}/../../datasets/MOM.Y2015_D002_S00000.inc.nc . 

C
C --- From CFSv2 interannual 
C
foreach f ( cfsv2_gom-sea_${YOF}_01hr_TaKqa.nc cfsv2_gom-sec_${YOF}_01hr_dswsfc.nc cfsv2_gom-sec_${YOF}_01hr_dlwsfc.nc  cfsv2_gom-sec_${YOF}_01hr_mslpPa.nc cfsv2_gom-sea_${YOF}_01hr_precip.nc cfsv2_gom-sec2_${YOF}_01hr_uv-10m.nc )
  touch  $f
  if (-z $f) then
    ${pget} ${S}/../../datasets/CFSv2/$f $f &
  endif
end
C
cd $S
C
C --- restart input, if needed
C
if (`grep "input_filename" input.nml | head -n 1 | awk '{if ($3 ~ "'r',") print 1; else print 0}'`) then
C
  mkdir -p       RESTART_${Y01}${A}
  touch          RESTART_${Y01}${A}/coupler.res
  if (-z         RESTART_${Y01}${A}/coupler.res) then
    ${pget} ${D}/RESTART_${YXX}${A}.tar.gz . &
  endif
  wait
  if (-z         RESTART_${Y01}${A}/coupler.res) then
    ${APRUN1} /bin/tar -xzvf RESTART_${YXX}${A}.tar.gz
  endif
C
C ---  Check to make sure restart file is there
C
  cd             RESTART_${Y01}${A}
C
  if (-z coupler.res) then
      echo "no restart for" $YF
      cd $D/..
      /bin/mv -f LIST LIST_BADRUN
      echo "BADRUN" > LIST
      exit
  else
    setenv RF `grep "Current" coupler.res | awk '{printf("%4.4d,%2.2d,%2.2d,%2.2d,%2.2d,%2.2d\n",$1,$2,$3,$4,$5,$6)}'`
    if ( $YF == $RF ) then
      echo "restarting on " $RF
    else
      echo "restarting on " $RF
      echo "but should be " $YF
      cd $D/..
      /bin/mv -f LIST LIST_BADRUN
      echo "BADRUN" > LIST
      exit
    endif
  endif
C end restart input
endif
C
C --- output directories
C
mkdir -p $S/RESTART
mkdir -p $S/RESTART_${YXX}${B}
mkdir -p $S/OUTPUT_${Y01}${A}
C
C --- executable
C
cd $S
/bin/rm -f                            MOM6
#/bin/cp ${D}/../../../../${V}/ice_ocean_SIS2_symmetric/repro/MOM6 .
#/bin/cp ${V}/ice_ocean_SIS2_symmetric/repro/MOM6 .
/bin/cp ${V}/ice_ocean-noaa-psd_SIS2_sym/repro/MOM6 .
C
C --- let all file copies complete.
C
wait
/bin/ls -laFq
/bin/ls -laFq INPUT
C
if ($NMPI == 0) then
C
C --- run the model, without MPI or SHMEM
C
if ($NOMP == 0) then
  setenv NOMP 1
endif
C
switch ($OS)
case 'Linux':
C
C   --- $NOMP CPUs/THREADs, if compiled for OpenMP.
C
    /bin/rm -f core
    touch core
    env OMP_NUM_THREADS=$NOMP MPSTKZ=8M ./MOM6
    breaksw
case 'HPE':
    limit stacksize unlimited
    setenv OMP_NUM_THREADS  $NOMP
    setenv OMP_STACKSIZE    127M
    ./MOM6
    breaksw
case 'AIX':
C
C   --- $NOMP CPUs/THREADs, if compiled for IBM OpenMP.
C
    /bin/rm -f core
    touch core
    setenv SPINLOOPTIME     500
    setenv YIELDLOOPTIME    500
    setenv XLSMPOPTS       "parthds=${NOMP}:spins=0:yields=0"
    ./MOM6
    breaksw
#case 'AIX':
#C
#C   --- $NOMP CPUs/THREADs, if compiled for KAI OpenMP.
#C
#    /bin/rm -f core
#    touch core
#    env OMP_NUM_THREADS=$NOMP ./MOM6
#    breaksw
endsw
else
C
C --- run the model, with MPI or SHMEM and perhaps also with OpenMP.
C
date +"MOM6 START  %c"
switch ($OS)
case 'Linux':
C
C   --- $NMPI MPI tasks and $NOMP THREADs, if compiled for OpenMP.
C
    /bin/rm -f core
    touch core
    setenv OMP_NUM_THREADS $NOMP
    mpirun -np $NMPI ./MOM6
    breaksw
case 'HPE':
    if ($NOMP == 0) then
#     48 cores per node, 24 cores per NUMA node
      setenv NMPI1  `expr $NMPI % 48`
      if ($NMPI1 == 0) then
        setenv NMPI1 48
      endif
      setenv NMPI11 `expr $NMPI1 + 1`
      setenv NMPI1S `expr $NMPI11 / 2`
      setenv NMPI1R `expr $NMPI1 - $NMPI1S`
      setenv NMPI1A `expr $NMPI1S - 1`
      setenv NMPI1B `expr $NMPI1R + 23`
      if     ($NMPI1 == 1) then
        setenv NMPIDSM "0:0-47:allhosts"
      else
        setenv NMPIDSM "0-${NMPI1A},24-${NMPI1B}:0-47:allhosts"
      endif
      echo $NMPIDSM
      setenv MPI_DISPLAY_SETTINGS       1
      setenv MPI_VERBOSE                1
      #setenv MPI_VERBOSE2              1
      #setenv MPI_BUFS_PER_HOST         768
      #setenv MPI_BUFS_PER_PROC         128
      setenv MPI_DSM_DISTRIBUTE         yes
      setenv MPI_DSM_CPULIST            "$NMPIDSM"
      #setenv MPI_DSM_VERBOSE           1
      setenv KMP_AFFINITY               disabled
      setenv OMP_NUM_THREADS            1
      mpiexec_mpt -np $NMPI ./MOM6
    else
      limit stacksize unlimited
      setenv MPI_DISPLAY_SETTINGS       1
      setenv MPI_VERBOSE                1
      setenv MPI_VERBOSE2               1
      #setenv MPI_BUFS_PER_HOST         768
      #setenv MPI_BUFS_PER_PROC         128
      setenv KMP_AFFINITY               disabled
      setenv OMP_NUM_THREADS            $NOMP
      setenv OMP_STACKSIZE              127M
      mpiexec_mpt -np $NMPI omplace -nt $NOMP ./MOM6
    endif
    breaksw
    case 'IDP':
# ---   From "Using IntelMPI on Discover"
# ---   https://modelingguru.nasa.gov/docs/DOC-1670
        setenv I_MPI_DAPL_SCALABLE_PROGRESS	1
        setenv I_MPI_DAPL_RNDV_WRITE		1
        setenv I_MPI_JOB_STARTUP_TIMEOUT	10000
        setenv I_MPI_HYDRA_BRANCH_COUNT		512
        setenv DAPL_ACK_RETRY		 7
        setenv DAPL_ACK_TIMER		 23
        setenv DAPL_RNR_RETRY		 7
        setenv DAPL_RNR_TIMER		 28
# ---   intel scaling suggestions
        setenv DAPL_CM_ARP_TIMEOUT_MS	 8000
        setenv DAPL_CM_ARP_RETRY_COUNT	 25
        setenv DAPL_CM_ROUTE_TIMEOUT_MS  20000
        setenv DAPL_CM_ROUTE_RETRY_COUNT 15
        setenv DAPL_MAX_CM_RESPONSE_TIME 20
        setenv DAPL_MAX_CM_RETRIES	 15
        if ($NOMP == 0) then
            setenv OMP_NUM_THREADS      1
            mpirun ./MOM6
        else
            setenv OMP_NUM_THREADS      $NOMP
            mpirun ./MOM6
        endif
        breaksw
case 'XC30':
    if ($NOMP == 0) then
      setenv NOMP 1
    endif
    setenv OMP_NUM_THREADS           $NOMP
    setenv MPI_COLL_OPT_ON           1
    setenv MPICH_RANK_REORDER_METHOD 1
    setenv MPICH_MAX_SHORT_MSG_SIZE  65536
    setenv MPICH_UNEX_BUFFER_SIZE    90M
    setenv MPICH_VERSION_DISPLAY     1
    setenv MPICH_ENV_DISPLAY         1
    setenv NO_STOP_MESSAGE
    if ($NOMP == 0 || $NOMP == 1) then
      setenv NMPI1  `expr $NMPI % 24`
      if ($NMPI1 == 0) then
        setenv NMPI1 24
      endif
      setenv NMPI2  `expr $NMPI - $NMPI1`
      setenv NMPI11 `expr $NMPI1 + 1`
      setenv NMPI1S `expr $NMPI11 / 2`
      time aprun -n $NMPI1 -S $NMPI1S ./MOM6 : -n $NMPI2 -d 1 ./MOM6
#     time aprun -n $NMPI -d 1 ./MOM6
    else if ($NOMP == 2) then
      time aprun -n $NMPI -d 2 ./MOM6
    else if ($NOMP == 3) then
      time aprun -n $NMPI -d 3 ./MOM6
    else if ($NOMP == 4) then
      time aprun -n $NMPI -d 4 ./MOM6
    endif
    breaksw
case 'XC40':
    if ($NOMP == 0) then
      setenv NOMP 1
    endif
    setenv OMP_NUM_THREADS           $NOMP
    setenv MPI_COLL_OPT_ON           1
    setenv MPICH_RANK_REORDER_METHOD 1
    setenv MPICH_MAX_SHORT_MSG_SIZE  65536
    setenv MPICH_UNEX_BUFFER_SIZE    90M
    setenv MPICH_VERSION_DISPLAY     1
    setenv MPICH_ENV_DISPLAY         1
    setenv NO_STOP_MESSAGE
    if ($NOMP == 0 || $NOMP == 1) then
#     32 cores per node, 16 cores per NUMA node
      setenv NMPI1  `expr $NMPI % 32`
      if ($NMPI1 == 0) then
        setenv NMPI1 32
      endif
      setenv NMPI2  `expr $NMPI - $NMPI1`
      setenv NMPI11 `expr $NMPI1 + 1`
      setenv NMPI1S `expr $NMPI11 / 2`
      time aprun -n $NMPI1 -S $NMPI1S ./MOM6 : -n $NMPI2 -d 1 ./MOM6
#     time aprun -n $NMPI -d 1 ./MOM6
    else if ($NOMP == 2) then
      time aprun -n $NMPI -d 2 ./MOM6
    else if ($NOMP == 3) then
      time aprun -n $NMPI -d 3 ./MOM6
     else if ($NOMP == 4) then
      time aprun -n $NMPI -d 4 ./MOM6
    endif
    breaksw
case 'AIX':
C
C   --- $NMPI MPI tasks and $NOMP THREADs, if compiled for IBM OpenMP.
C
    /bin/rm -f core
    touch core
    setenv SPINLOOPTIME		500
    setenv YIELDLOOPTIME	500
    setenv XLSMPOPTS		"parthds=${NOMP}:spins=0:yields=0"
    setenv MP_SHARED_MEMORY	yes
    setenv MP_SINGLE_THREAD	yes
#   setenv MP_SINGLE_THREAD	no
    setenv MP_EAGER_LIMIT	65536
#   setenv MP_EUILIB		us
#   list where the MPI job will run
#   env MP_LABELIO=YES $POE hostname
    time $POE ./MOM6
    breaksw
#case 'AIX':
#C
#C   --- $NMPI MPI tasks and $NOMP THREADs, if compiled for KAI OpenMP.
#C
#    /bin/rm -f core
#    touch core
#    setenv OMP_NUM_THREADS	$NOMP
#    setenv MP_SHARED_MEMORY	yes
#    setenv MP_SINGLE_THREAD	yes
#    setenv MP_EAGER_LIMIT	65536
#    setenv MP_EUILIB		us
#    setenv MP_EUIDEVICE		css0
##   list where the MPI job will run
#    env MP_LABELIO=YES $POE hostname
#    time $POE ./MOM6
#    breaksw
default:
    echo "This O/S," $OS ", is not configured for MPI/SHMEM"
    exit (1)
endsw
endif
date +"MOM6 END    %c"
C
C --- restart output
C
touch   RESTART/coupler.res
/bin/mv RESTART/[ciM]*      RESTART_${YXX}${B}
C
C --- build and run or submit the restart tar script
C
if ( ${B} == "a" ) then
  awk -f $D/../${E}.awk y01=${Y01} ab=${A} $D/../${E}Ar.csh >! RESTART_${YXX}${B}.csh
  ~wallcraf/bin/q_navo RESTART_${YXX}${B}.csh
endif
C
C --- clean up the output
C
touch   dummy.nc
/bin/mv *.nc*          OUTPUT_${Y01}${A}
/bin/mv logfile*       OUTPUT_${Y01}${A}
/bin/mv time_stamp.out OUTPUT_${Y01}${A}
C
C --- MOM6 error stop is implied by the absence of a restart.
C
if (-z RESTART_${YXX}${B}/coupler.res) then
  cd $D/..
  /bin/mv LIST LIST_BADRUN
  echo "BADRUN" > LIST
endif
C
C --- submit postprocessing scripts
C --- 1 - daily archm and monthly means
C
#cd $HOME/MOM6/${R}/postproc
#setenv X `echo ${E} | awk '{printf("%04.1f", $1*0.1)}'`
#C
#/bin/rm -f             pp_archm_${E}_${Y01}${A}.{csh,log}
#awk -f postproc.awk y=${Y01} p=${A} r=${R} e=${E} x=${X} t=${T} k=${K} \
#       pp_archm.csh >! pp_archm_${E}_${Y01}${A}.csh
#~wallcraf/bin/q_navo   pp_archm_${E}_${Y01}${A}.csh
#C
#/bin/rm -f postproc_intann_mnsqe_${E}_${Y01}${A}.{com,log}
#awk -f postproc.awk y=${Y01} p=${A} r=${R} e=${E} x=${X} t=${T} k=${K} \
#       postproc_intann_mnsqe.csh >! postproc_intann_mnsqe_${E}_${Y01}${A}.csh
#~wallcraf/bin/q_navo postproc_intann_mnsqe_${E}_${Y01}${A}.csh
#C
#C --- 2 - plots
#C
#/bin/rm -f postproc_intann_plot_${E}_${Y01}${A}.{com,log}
#awk -f postproc.awk y=${Y01} p=${A} r=${R} e=${E} x=${X} t=${T} k=${K} \
#       postproc_intann_plot.csh >! postproc_intann_plot_${E}_${Y01}${A}.csh
#~wallcraf/bin/q_navo postproc_intann_plot_${E}_${Y01}${A}.csh
#C
#C --- 3 - sample transports
#C
#/bin/rm -f postproc_intann_tprt_${E}_${Y01}${A}.{com,log}
#awk -f postproc.awk y=${Y01} p=${A} r=${R} e=${E} x=${X} t=${T} k=${K} \
#       postproc_intann_tprt.csh >! postproc_intann_tprt_${E}_${Y01}${A}.csh
#~wallcraf/bin/q_navo postproc_intann_tprt_${E}_${Y01}${A}.csh
#C
#C --- 4 - data2d extraction, moorings, ice creation and plotting
#C
#/bin/rm -f postproc_intann_data2d_${E}_${Y01}${A}.{com,log}
#awk -f postproc.awk y=${Y01} p=${A} r=${R} e=${E} x=${X} t=${T} k=${K} \
#       postproc_intann_data2d.csh >! postproc_intann_data2d_${E}_${Y01}${A}.csh
#~wallcraf/bin/q_navo postproc_intann_data2d_${E}_${Y01}${A}.csh
#C
#C --- 5 - GOMb0.08 to GLBu0.08 to netCDF
#C
##/bin/rm -f postproc_intann_GLBu0.08_${E}_${Y01}${A}.{com,log}
##awk -f postproc.awk y=${Y01} p=${A} r=${R} e=${E} x=${X} t=${T} k=${K} \
##       postproc_intann_GLBu0.08.csh >! postproc_intann_GLBu0.08_${E}_${Y01}${A}.csh
##~wallcraf/bin/q_navo postproc_intann_GLBu0.08_${E}_${Y01}${A}.csh
C
C --- wait for tar bundles to complete
C
wait
C
C  --- END OF MODEL RUN SCRIPT
C
date +"END    %c"
