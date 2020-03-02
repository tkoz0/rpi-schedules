# rpi-schedules
class schedules scraped from sis.rpi.edu

saving pages to use

1. log into sis -> student menu -> class search
2. pick a semester, select all subjects, and search for sections
3. save the page (html only)

processing pages

1. place raw pages in a directory and make a new directory for scrubbed output
2. run ``python3 page_scrubber.py <input dir> <output dir>``

converting to json data

1. use directory of raw pages from previous step
2. run ``python3 page_to_json.py <input dir> <output dir>``

schema for json data

- file contents (root level of the json data)  
    ``{``  
    ``"Computer Science": [COURSE_OBJ, ...],``  
    ``...``  
    ``}``
- COURSE_OBJ (one per course section)  
    ``{``  
    ``"select": "NR",``  
    ``"crn": 14160,``  
    ``"code": "CSCI",``  
    ``"number": 1100,``  
    ``"section": "01",``  
    ``"campus": "T",``  
    ``"credits": 4.0,``  
    ``"title": "COMPUTER SCIENCE I",``  
    ``"days": "MR",``  
    ``"time_beg": [10,30],``  
    ``"time_end": [12,10],``  
    ``"profs": ["Uzma Mushtaque","Erica Ann Eberwein","Shianne M. Hulbert"],``  
    ``"date_beg": [5,20],``  
    ``"date_end": [8,16],``  
    ``"location": "DARRIN 330",``  
    ``"attributes": "Introductory Level Course",``  
    ``"seats": {SEATS_OBJ}``  
    ``}``
- SEATS_OBJ (data on course seats)  
    ``{``  
    ``"cap": 30,``  
    ``"act": 12,``  
    ``"rem": 18,``  
    ``"wl_cap": 0,``  
    ``"wl_act": 0,``  
    ``"wl_rem": 0,``  
    ``"cl_cap": 0,``  
    ``"cl_act": 0,``  
    ``"cl_rem": 0``  
    ``}``

schema notes

- some items may not be provided, in these cases their values are null
- course section is a string, some contain letters and it preserves leading 0
- credits is a float since that is what the original format uses
- days has letters (M=monday, T=tuesday, W=wednesday, R=thursday, F=friday)
- begin and end times are list of 2 numbers in 24 hour time
- professors list has primary professor first followed by others
- begin and end dates are list of 2 numbers [month,day]
