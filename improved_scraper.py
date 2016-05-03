import os
import sys

import urllib2
from bs4 import BeautifulSoup
import re
import json


TERM_CODES = [1122,1124,1134,1142,1144,1154, 1162, 1164]
TERM_CODES_NAMES = ['Fall_11', 'Spring_12', 'Spring_13','Fall_13', 'Spring_14','Spring_15', 'Fall_15', 'Spring_16']
TERM_CODE_DICT = {code:name for code, name in zip(TERM_CODES, TERM_CODES_NAMES)}
CURRENT_TERM_CODE = TERM_CODES[-1]

REGISTRAR_URL_PREFIX = "http://registrar.princeton.edu/course-offerings/"
COURSE_LISTINGS_URL_TEMPLATE = REGISTRAR_URL_PREFIX + "search_results.xml?term={term}"
COURSE_URL_TEMPLATE = REGISTRAR_URL_PREFIX + "course_details.xml?courseid={courseid}&term={term}"

COURSE_URL_REGEX = re.compile(r'courseid=(?P<id>\d+)')
PROF_URL_REGEX = re.compile(r'dirinfo\.xml\?uid=(?P<id>\d+)')
LISTING_REGEX = re.compile(r'(?P<dept>[A-Z]{3})\s+(?P<num>\d{3})')

def get_course_ids(term_id):
  "Returns all course ids by looking at the registrar listing of all classes for the term term_id"
  course_listings_url = COURSE_LISTINGS_URL_TEMPLATE.format(term=term_id)
  course_listings_page = urllib2.urlopen(course_listings_url).read()
  soup = BeautifulSoup(course_listings_page, "lxml")
  links = soup('a', href=COURSE_URL_REGEX)
  courseids = [COURSE_URL_REGEX.search(a['href']).group('id') for a in links]
  return set(courseids)

def fetch_all(term_id):
  """Fetches all class pages in the registrar for the term term_id, 
  and stores the html files in a directory named by TERM_CODES_NAMES for the term specified"""
  courseids = get_course_ids(term_id)
  directory_path = TERM_CODE_DICT[term_id]
  if not os.path.exists(directory_path):
    os.makedirs(directory_path)

  cur_files = os.listdir(directory_path)
  print '%d of %d files already indexed' % (len(cur_files), len(courseids))
  for i, courseid in enumerate(courseids):
    if '{courseid}.html'.format(courseid=courseid) not in cur_files:
      print 'Retrieving index #: %d, courseid:%s' % (i, courseid)
      course_url = COURSE_URL_TEMPLATE.format(term=term_id, courseid=courseid)
      course_page = urllib2.urlopen(course_url).read()

      file_path = '{directory_path}/{courseid}.html'.format(directory_path=directory_path, courseid=courseid)
      f = open(file_path, 'w')
      f.write(course_page)


def scrape_page(page):
  "Returns a dict containing as much course info as possible from the HTML contained in page."
  soup = BeautifulSoup(page, 'lxml').find('div', id='timetable') # was contentcontainer
  course = get_course_details(soup)
  course['listings'] = get_course_listings(soup)
  course['profs'] = get_course_profs(soup)
  course['classes'] = get_course_classes(soup)
  return course


def clean(str):
  "Return a string with leading and trailing whitespace gone and all other whitespace condensed to a single space."
  if str != None: 
      return re.sub('\s+', ' ', str.strip())
  else:
      return ''
def flatten(dd):
  s = ""
  try:
    for i in dd.contents:
      try:
        s += i
      except:
        s += flatten(i)
  except:
    s += "oh, dear"
  return s

def get_course_details(soup):
  "Returns a dict of {courseid, area, title, descrip, prereqs}."
  # import pdb; pdb.set_trace()
  try:
    area = clean(soup('strong')[1].next_sibling)
  except TypeError:
    area = ''
  # course_num_soup = soup('strong')[1]
  # pdf_npdf = clean(course_num_soup.findNext('em').string)
  # area = clean(course_num_soup.findNext().string)
  # if pdf_npdf == area:
  # 	area = ''
  if re.match(r'^\((LA|SA|HA|EM|EC|QR|STN|STL)\)$', area):
    area = area[1:-1]
  else:
    area = ''

  match = re.match(r'\(([A-Z]+)\)', clean(soup('strong')[1].findNext(text=True)))
  pretitle = soup.find(text=re.compile("Prerequisites"))
  descrdiv = soup.find('div', id='descr')

  title = clean(soup('h2')[0].string)
  # if 'Optimization' in title:
  # 	import pdb; pdb.set_trace()
  return {
    'courseid': COURSE_URL_REGEX.search(soup.find('a', href=COURSE_URL_REGEX)['href']).group('id'),
    'area': area, #bwk: this was wrong[1:-1],    # trim parens #  match.group(1) if match != None else ''
    'title': title,  # was [1]
    ###'descrip': clean(descrdiv.contents[0] if descrdiv else ''),
    'descrip': clean(flatten(descrdiv)),
    'prereqs': clean(pretitle.parent.findNextSibling(text=True)) if pretitle != None else '' # broken spring 16 for many courses
  } 

def get_course_listings(soup):
  "Return a list of {dept, number} dicts under which the course is listed."
  listings = soup('strong')[1].string
  return [{'dept': match.group('dept'), 'number': match.group('num')} for match in LISTING_REGEX.finditer(listings)]

def get_course_profs(soup):
  "Return a list of {uid, name} dicts for the professors teaching this course."
  prof_links = soup('a', href=PROF_URL_REGEX)
  return [{'uid': PROF_URL_REGEX.search(link['href']).group('id'), 'name': clean(link.string)} for link in prof_links]

def get_single_class(row):
  "Helper function to turn table rows into class tuples."
  cells = row('td')
  time = cells[2].string.split("-")
  bldg_link = cells[4].strong.a

  # <td><strong>Enrolled:</strong>0
  # <strong> Limit:</strong>11</td>
  enroll = ''
  limit = ''
  if cells[5] != None:    # bwk
    enroll = cells[5].strong.nextSibling.string.strip()

    limit = cells[5].strong.nextSibling.nextSibling.nextSibling
    if limit != None:
      limit = limit.string.strip()
    else:
      limit = "0"

  return {
    'classnum': cells[0].strong.string,
    'section': cells[1].strong.string,
    'days': re.sub(r'\s+', '', cells[3].strong.string),
    'starttime': time[0].strip(),
    'endtime': time[1].strip(),
    'bldg': bldg_link.string.strip(),
    'roomnum': bldg_link.nextSibling.string.replace('&nbsp;', ' ').strip(),
    'enroll': enroll, # bwk
    'limit': limit   #bwk
  }

def get_course_classes(soup):
  "Return a list of {classnum, days, starttime, endtime, bldg, roomnum} dicts for classes in this course."
  class_rows = soup('tr')[1:] # the first row is actually just column headings
  # This next bit tends to cause problems because the registrar includes precepts and canceled
  # classes. Having text in both 1st and 4th columns (class number and day of the week)
  # currently indicates a valid class.
  return [get_single_class(row) for row in class_rows if row('td')[0].strong and row('td')[3].strong.string]



def process_all(term_id):
  directory_path = TERM_CODE_DICT[term_id]
  cur_files = os.listdir(directory_path)
  out_file_name = directory_path.lower()+'.json'
  out_file = open(out_file_name, 'w')
  out_file.write('[\n')
  for i, file_name in enumerate(cur_files):
    file_path = '%s/%s' % (directory_path, file_name)
    f = open(file_path)
    page = f.read()
    page_data = scrape_page(page)
    page_data['termid'] = str(term_id)
    json.dump(page_data, out_file)
    if i < len(cur_files) - 1:
      out_file.write(',\n')
  out_file.write(']\n')
# process_all(1164)