#Synopsis
This is a Python script that will take a folder full of AnFutures CSV future files along with an index file and aggregate into one CSV file.

#Motivation
Every futures contract consist of 3 months of 1 minute data. With over 17 years worth of files (71 actually in my case), I needed a way to sort order by timestamp into one CSV file so that it could be imported into a database (either relational or time series).

#Requirements
- Python 3.x
- Linux or Windows O/S

#Installation
Create a directory on your Linux box

```
cd /
mkdir /anfutures
cd anfutures
mkdir /csv
cd csv
mkdir 1m
```

- Copy all the AnFuture CSV files into /anfutures/csv/1m
- Create an index.lst file with your text editor inside this directory
- Include on each line the filename of the CSV file you need to process
- The files MUST be listed in date order from earliest to latest to achieve proper sorting of the data points
- A list file is needed because unfortunately a folder walk won't work due to the incorrect sorting of 1998/1999 at the end of the directory listing being procssed last (which is wrong data order wise)
- See the example index.lst file for proper setup.

#Usage
```
python anf2csv.py dirPath
```
*dirPath is the path that points at the folder containing the AnFutures CSV and index.lst files*

Based on the folder structure in the installation:
```
cd /anfutures/csv/1m
python anf2csv.py .
```

#Performance Notes
Windows 10 Home 64-bit
  - AMD 64-bit Phenom II X6 1055T 2.8Ghz 6 core 
  - 16 GB RAM
  - 640GB WDC SATA 3Gb/s
  - 71 AnFutures CSV 1 minute ES mini files from 1998 to 2015
  - 5,052,606 data points
  - 115 seconds
  - 304MB result file size
  - Python 3.5.1

Ubuntu Server 14.04 LTS
  - AMD 64-bit FX 8310 8 core
  - 32 GB RAM
  - 1 TB WDC SATA 3Gb/s
  - 71 AnFutures CSV 1 minute ES mini files from 1998 to 2015
  - 5,052,606 data points
  - 35.46 seconds
  - 307MB result file size
  - Python 3.4.0


#Output Format of Resultant File
The resulting CSV file is in the following format:
```
YYYY/MM/DD HH:MM, Open, High, Low, Close, Volume, CC Close
```

There is NO header generated.

I strip out the symbol and intraday marker as its redundant and just takes up a lot of disk space. The timestamp is patched together from the date and time columns. If you need to create another timestamp format, simply modify the code to do so as its pretty self explanatory.
