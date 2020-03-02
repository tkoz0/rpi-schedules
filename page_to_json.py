from bs4 import BeautifulSoup
from bs4.element import NavigableString
import sys
import os
import json

# usage: page_to_json.py <input dir> <output dir>
inDir = sys.argv[1]
outDir = sys.argv[2]
if inDir[-1] != '/': inDir += '/'
if outDir[-1] != '/': outDir += '/'

def parseTime(s):
    s = s.strip()
    t = list(map(int,s[:-2].split(':')))
    if s.endswith('am'):
        if t[0] == 12: t[0] = 0
    elif s.endswith('pm'):
        if t[0] != 12: t[0] += 12
    else: assert 0
    assert len(t) == 2 and 0 <= t[0] < 24 and 0 <= t[1] < 60
    return t

def makeCourse(row):
    # process more complex data first
    assert len(row) == 23
    
    # time, may not be provided
    try:
        time = row[9].contents[0].strip().split('-')
        assert len(time) == 2
        time = list(map(parseTime,time))
    except: # time TBA
        assert row[9].contents[0].contents[0].strip() == 'TBA'
        time = None
    
    # profs, could be TBA
    try:
        profs = [p for p in row[19].contents
                if type(p) == NavigableString]
        assert len(profs) == 2
        assert profs[0].endswith('(') and profs[1].startswith(')')
        profs[0] = profs[0][:-1]
        profs[1] = profs[1][1:]
        profs = [p.strip() for p in ''.join(profs).split(',')]
    except: # profs TBA
        assert row[19].contents[0].contents[0].strip() == 'TBA'
        profs = []
    
    # dates, may not be provided
    dates = row[20].contents[0].strip().split('-')
    dates = [list(map(int,d.split('/'))) for d in dates]
    assert len(dates) == 2 == len(dates[0]) == len(dates[1])
    assert 1 <= dates[0][0] <= 12 and 1 <= dates[1][0] <= 12
    assert 1 <= dates[0][1] <= 31 and 1 <= dates[1][1] <= 31
    
    # location, could be TBA
    try:
        location = row[21].contents[0].strip()
    except:
        assert row[21].contents[0].contents[0].strip() == 'TBA'
        location = None
    
    # simpler data
    
    # "select" column, could be empty
    try: select = row[0].contents[0].contents[0].strip()
    except: select = None
    # crn
    try:
        crn = row[1].contents[0].contents[0].strip()
        crn = int(crn)
        if type(crn) != int: print('ERROR:crn not int');quit()
    except: crn = None
    
    # build dictionary object
    return {
    'select':   select, # within abbr tag
    'crn':      crn, # within a tag
    'code':     row[2].contents[0].strip(),
    'number':   int(row[3].contents[0]),
    'section':  row[4].contents[0].strip(),
    'campus':   row[5].contents[0].strip(),
    'credits':  float(row[6].contents[0]),
    'title':    row[7].contents[0].strip(),
    'days':     row[8].contents[0].strip(),
    'time_beg': None if time == None else time[0],
    'time_end': None if time == None else time[1],
    'profs':    profs,
    'date_beg': dates[0],
    'date_end': dates[1],
    'location': location,
    'attributes': row[22].contents[0].strip(),
    'seats': {
        'cap': int(row[10].contents[0]),
        'act': int(row[11].contents[0]),
        'rem': int(row[12].contents[0]),
        'wl_cap': int(row[13].contents[0]),
        'wl_act': int(row[14].contents[0]),
        'wl_rem': int(row[15].contents[0]),
        'cl_cap': int(row[16].contents[0]),
        'cl_act': int(row[17].contents[0]),
        'cl_rem': int(row[18].contents[0]),
        }
    }

for file in os.listdir(inDir):
    
    # pull row data out of the scrubbed page
    bs4page = BeautifulSoup(open(inDir+file,'rb').read(),'html.parser')
    dataTable = bs4page.contents[2].contents[0]
    dataTableRows = [row for row in dataTable if row.name == 'tr']
    
    jsonData = dict() # file root in the schema
    currentGroup = None # name of subject/department
    currentCourses = [] # courses list
    
    for row in dataTableRows:
        row = [c for c in row if c.name in ['th','td']] # get table cells
        if len(row) == 1: # new subject/department header
            if currentGroup: # save previous subject/department
                assert not (currentGroup in jsonData)
                jsonData[currentGroup] = currentCourses
            currentGroup = row[0].contents[0]
            currentCourses = []
        elif row[0].name == 'th': # skip header rows
            continue
        else: # course row
            currentCourses.append(makeCourse(row))
            #except:print(file);print('\n'.join(str(d)for d in row));quit()
            # TODO issue is courses spanning multiple rows
    
    assert not (currentGroup in jsonData)
    jsonData[currentGroup] = currentCourses
    
    # write json data to output file
    dotI = len(file)-1
    while dotI >= 0 and file[dotI] != '.': dotI -= 1
    outFileName = file+'.json' if dotI == -1 else file[:dotI]+'.json'
    outFile = open(outDir+outFileName,'w')
    outFile.write(json.dumps(jsonData,indent=4,sort_keys=True))
    outFile.write('\n')
    outFile.close()
