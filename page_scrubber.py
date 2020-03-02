from bs4 import BeautifulSoup
import sys
import os

# usage: page_scrubber.py <input dir> <output dir>
inDir = sys.argv[1]
outDir = sys.argv[2]
if inDir[-1] != '/': inDir += '/'
if outDir[-1] != '/': outDir += '/'

for file in os.listdir(inDir):
    
    # reduce page to just the data table
    bs4page = BeautifulSoup(open(inDir+file,'rb').read(),'html.parser')
    dataTable = bs4page.find_all('table',class_='datadisplaytable')[0]
    html = bs4page.find_all('html')[0]
    html.contents = ['\n',dataTable,'\n']
    table = bs4page.find_all('table',class_='datadisplaytable')[0]
    table.contents = table.contents[2:] # remove "sections found" text
    
    # write scrubbed file
    outFile = open(outDir+file,'w')
    outFile.write(str(bs4page))
    outFile.close()
