# This file will append a time axis to all the TRMM nc4 files present in the folder
# using the name of the file 
import os, glob

for filename in glob.glob('*.nc4'):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
        s = filename
        year = int(re.findall("\d+", s)[2][0:4])
        month = int(re.findall("\d+", s)[2][4:6])
        date = int(re.findall("\d+", s)[2][6:8])
        time = int(re.findall("\d+", s)[3])
        print(time)
        #os.system("cdo griddes %s" %filename)
        os.system("cdo -r -f nc settaxis,%d-%d-%d,%d:00:00,1hour %s o.nc" %(year, month, date, time, filename))
        os.system("mv o.nc %s" %filename)
