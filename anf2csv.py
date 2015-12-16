# File: anf2csv.py
# Purpose: Filters, orders, and converts AnFutures CSV files into one CSV file
# Company: Kobashi Computing
# Author: Kerry Kobashi
#
# Use:
#   anf2csv dirPath
#
# The dirPath is where the index.lst and all the CSV files are located
# The index.lst file:
#   Contains one file per line
#   Do NOT insert empty lines or have a trailing empty line in the file
#   The file order must be sorted according to date
# The output file is result.csv

import sys
import os
import csv
import time

numArgs = len(sys.argv)
if numArgs != 2:
    print("Wrong command line syntax:")
    print("  anf2csv dirPath")
    exit(1)

dirPath = sys.argv[1]
if not os.path.isdir(dirPath):
    print("The directory path specified does not exist")
    exit(1)

indexFilePath = os.path.join(dirPath, "index.lst")
if not os.path.isfile(indexFilePath):
    print("The index file does not exist")
    exit(1)

# Process the index file
# It holds the correct sort order in date/time sequence of the filenames and data
indexFile = open(indexFilePath, "r")
lines = indexFile.readlines()
numFiles = len(lines)
indexFile.close()

print(str(numFiles) + " AnFutures CSV files to process")
startTime = time.time()

fileCount = 0
rowCount = 0
outfilePath = os.path.join(dirPath, "result.csv")
outfile = open(outfilePath, "w+")

for filename in lines:
    filePath = os.path.join(dirPath, filename.rstrip())

    # Input: Symbol, Intraday marker, YYMMDD, HH:MM, Open, High, Low, Close, Volume, CC Close
    infile = open(filePath, "r")
    csvReader = csv.reader(infile)
    csvWriter = csv.writer(outfile, delimiter=',')
    fileCount += 1
    print("Processing file " + str(fileCount) + " of " + str(numFiles) + ": " + filePath)

    for row in csvReader:
        # Output: YYYY/MM/DD, HH:MM, Open, High, Low, Close, Volume, CC Close
        # Ignore Symbol and intraday marker
        # Strip out leading zeros and force 2 digit precision in prices
        #
        # writerow needs a list of strings, not a string so we create an empty list and append strings
        # to the list one by one
        # [YYYY/MM/DD HH:MM, Open, High, Low, Close, Volume, CC Close]
        strList = []

        # input of date is unfortunately deficient because it is not four placeholders for the year
        # and you can't tell the difference between 1999 and 2099
        # So we have to make special case assumptions that:
        #   98MMDD is 1998
        #   99MMDD is 1999
        #
        # OpenTSDB timestamp we will cater our CSV result to it:
        #   YYYY/MM/DD HH:MM

        year = row[2]
        yy = year[:2]
        if yy in ["98", "99"]:
            yyyy = "19" + yy
        else:
            yyyy = "20" + yy

        timestamp = yyyy + "/" + year[2:4] + "/" + year[4:6] + " " + row[3]
        strList.append(timestamp)
        strList.append("%.2f" % float(row[4]))
        strList.append("%.2f" % float(row[5]))
        strList.append("%.2f" % float(row[6]))
        strList.append("%.2f" % float(row[7]))
        strList.append(row[8])
        strList.append("%.2f" % float(row[9]))
        csvWriter.writerow(strList)
        rowCount += 1

    infile.close()

outfile.close()
endTime = time.time()
print("Total processing time: " + "%.2f" % (endTime - startTime) + " seconds")
print("Total rows processed: " + format(rowCount, ",d"))


