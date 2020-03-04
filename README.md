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

1. Select (registration availability: C or NR for old data)
2. CRN (class registration number: 5 digits or blank)
3. Subj (subject code: 4 capital letters or blank)
4. Crse (course number, 4 digits or blank)
5. Sec (course section, usually 2 digits but can contain letters or be blank)
6. Cmp (campus: H, T, or D, could be blank)
7. Cred (credits: floating point, may be a range separated by - or /)
8. Title (course title: possibly blank)
9. Days (course meeting day(s): letters MTWRFS, could be TBA or blank)
10. Time (course meeting time: either TBA or "hh:mm am-hh:mm pm" format)
11. Cap (section capacity: integer or blank)
12. Act (section actual: integer or blank)
13. Rem (section remaining: integer or blank)
14. WL Cap (waitlist capacity: integer or blank)
15. WL Act (waitlist actual: integer or blank)
16. WL Rem (waitlist remaining: integer or blank)
17. XL Cap (crosslist capacity: integer or blank)
18. XL Act (crosslist actual: integer or blank)
19. XL Rem (crosslist remaining: integer or blank)
20. Instructor (instructors: TBA or comma separated list, first ends with "(P)")
21. Date (MM/DD) (date range: MM/DD format)
22. Location (meeting room: TBA or building, possibly followed by room)
23. Attribute (note about course: could be blank)

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
