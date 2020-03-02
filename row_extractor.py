from bs4 import BeautifulSoup
from bs4.element import NavigableString
import sys
import os
import csv

# usage: page_to_json.py <input dir> <output dir>
inDir = sys.argv[1]
outDir = sys.argv[2]
if inDir[-1] != '/': inDir += '/'
if outDir[-1] != '/': outDir += '/'

def colspan(c): return int(c['colspan']) if c.has_attr('colspan') else 1

def extractText(item):
    if type(item) == NavigableString: return str(item)
    return ''.join(extractText(i) for i in item.contents)

for file in os.listdir(inDir):
    
    # pull row data out of the scrubbed page
    bs4page = BeautifulSoup(open(inDir+file,'rb').read(),'html.parser')
    dataTable = bs4page.contents[2].contents[0]
    dataTableRows = [row for row in dataTable if row.name == 'tr']
    
    # setup writer for the output file
    dotI = len(file)-1
    while dotI >= 0 and file[dotI] != '.': dotI -= 1
    outFileName = file+'.csv' if dotI == -1 else file[:dotI]+'.csv'
    outFile = open(outDir+outFileName,'w')
    csvWriter = csv.writer(outFile)
    
    # write rows to csv file
    for row in dataTableRows:
        row = [c for c in row if c.name in ['th','td']]
        if len(row) == 1: # subject/department header
            assert type(row[0].contents[0]) == NavigableString
            csvWriter.writerow([str(row[0].contents[0])])
        elif row[0].name == 'th': # skip header rows
            continue
        else: # course row
            row_strs = sum([[extractText(c)]*colspan(c) for c in row],[])
            assert len(row_strs) == 23
            csvWriter.writerow(row_strs)
    
    outFile.close()
