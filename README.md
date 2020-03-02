# rpi-schedules
class schedules scraped from sis.rpi.edu

saving pages to use
1. log into sis -> student menu -> class search
2. pick a semester, select all subjects, and search for sections
3. save the page (html only)

processing pages
1. place raw pages in a directory and make a new directory for scrubbed output
2. run ``python3 page_scrubber.py <input dir> <output dir>``

