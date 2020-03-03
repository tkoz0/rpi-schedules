# rpi-schedules
class schedules scraped from sis.rpi.edu

saving pages to use

1. log into sis -> student menu -> class search
2. pick a semester, select all subjects, and search for sections
3. save the page (html only)

extracting rows as csv

1. place raw pages in a directory and make a new directory for scrubbed output
2. run ``python3 page_scrubber.py <raws dir> <scrubbed dir>``
3. run ``python3 row_extractor.py <scrubbed dir> <csv dir>``

converting to json data (not done yet)

1. use directory of csv files from previous step

schema for csv data: length 1 rows = subject headers, other rows = 23 columns

1. Select (registration availability, C or NR for old data)
2. CRN (class registration number, 5 digits)
3. Subj (subject code, 4 capital letters)
4. Crse (course number, 4 digits)
5. Sec (course section, 2 digits)
6. Cmp (campus, H or T for Hartford or Troy)
7. Cred (credits, floating point, may be a range)
8. Title (course title)
9. Days (course meeting day(s), MTWRF)
10. Time (course meeting time, a range with am or pm)
11. Cap (section capacity)
12. Act (section actual)
13. Rem (section remaining)
14. WL Cap (waitlist capacity)
15. WL Act (waitlist actual)
16. WL Rem (waitlist remaining)
17. XL Cap (crosslist capacity)
18. XL Act (crosslist actual)
19. XL Rem (crosslist remaining)
20. Instructor (instructors separated by comma, primary (first) ends with "(P)")
21. Date (MM/DD) (date range for course)
22. Location (building followed by room)
23. Attribute (note about course, may be empty)

schema for csv notes:

1. courses map span multiple rows for meeting times on different days that are
at different times, possibly with different instructors or rooms, date range
should be the same

schema for json data (not finalized)

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
