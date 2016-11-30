import os
import sys

import urllib2
from bs4 import BeautifulSoup
import re
import json

REGISTRAR_URL_PREFIX = "http://registrar.princeton.edu/course-offerings/"
COURSE_URL_TEMPLATE = REGISTRAR_URL_PREFIX + "course_details.xml?courseid={courseid}&term={term}"
COURSE_URL_REGEX = re.compile(r'courseid=(?P<id>\d+)')
COURSE_RATINGS_TEMPLATE = "https://reg-captiva.princeton.edu/chart/index.php?terminfo={term}&courseinfo={courseid}"


class CourseRegistrarDownloader(object):
    COURSE_LISTINGS_URL_TEMPLATE = REGISTRAR_URL_PREFIX + "search_results.xml?term={term}"

    def __init__(self, root_output_path, verbose=False):
        self.root_output_path = root_output_path
        self.verbose = verbose

    def get_output_path(self, semester, year):
        sem = semester.lower()
        assert (sem == "fall" or sem == "spring")
        assert (year > 2000)
        return "{0}{1}_{2}".format(self.root_output_path, sem, year)

    @staticmethod
    def get_term_id(semester, year):
        sem = semester.lower()
        assert (sem == "fall" or sem == "spring")
        assert (year > 2000)
        base = 1000
        year_num = (year % 2000) * 10
        sem_num = 12 if sem == "fall" else 4
        return base + year_num + sem_num

    def get_course_ids(self, semester, year):
        """Returns all course ids by looking at the registrar listing
        of all classes for the term term_id"""
        if self.verbose:
            print "Getting Course IDs for", semester, year
        term_id = CourseRegistrarDownloader.get_term_id(semester, year)
        course_listings_url = self.COURSE_LISTINGS_URL_TEMPLATE.format(
            term=term_id)
        course_listings_page = urllib2.urlopen(course_listings_url).read()
        soup = BeautifulSoup(course_listings_page, "lxml")
        links = soup('a', href=COURSE_URL_REGEX)
        courseids = [
            COURSE_URL_REGEX.search(a['href']).group('id') for a in links
        ]
        return set(courseids)

    def fetch_all(self, semester, year, redownload=False):
        """Fetches all class pages in the registrar for the term term_id,
        and stores the html files in a directory named by TERM_CODES_NAMES
        for the term specified"""
        term_id = CourseRegistrarDownloader.get_term_id(semester, year)
        courseids = self.get_course_ids(semester, year)
        directory_path = self.get_output_path(semester, year)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        cur_files = os.listdir(directory_path)
        if self.verbose:
            print '%d of %d files already indexed' % (len(cur_files),
                                                      len(courseids))
        num_to_process = len(courseids) - len(cur_files)
        for i, courseid in enumerate(courseids):
            if '{0}.html'.format(courseid) not in cur_files or redownload:
                if self.verbose:
                    print 'Retrieving %d / %d, courseid:%s' % (
                        i, num_to_process, courseid)
                course_url = COURSE_URL_TEMPLATE.format(
                    term=term_id, courseid=courseid)
                course_page = urllib2.urlopen(course_url).read()

                file_path = '{directory_path}/{courseid}.html'.format(
                    directory_path=directory_path, courseid=courseid)
                f = open(file_path, 'w')
                f.write(course_page)


class CourseScraper(object):
    PROF_URL_REGEX = re.compile(r'dirinfo\.xml\?uid=(?P<id>\d+)')
    LISTING_REGEX = re.compile(r'(?P<dept>[A-Z]{3})\s+(?P<num>\d{3})')

    def __init__(self):
        pass

    def scrape_page(self, page):
        """Returns a dict containing as much course info as possible from
        the HTML contained in page."""
        soup = BeautifulSoup(page, 'lxml').find(
            'div', id='timetable')  # was contentcontainer
        course = self.get_course_details(soup)
        course['listings'] = self.get_course_listings(soup)
        course['profs'] = self.get_course_profs(soup)
        course['classes'] = self.get_course_classes(soup)
        return course

    @staticmethod
    def clean(my_str):
        """Returns a string with leading and trailing whitespace gone and
        all other whitespace condensed to a single space."""
        if my_str is not None:
            return re.sub('\s+', ' ', my_str.strip())
        else:
            return ''

    @staticmethod
    def flatten(dd):
        s = ""
        try:
            for i in dd.contents:
                try:
                    s += i
                except:
                    s += CourseScraper.flatten(i)
        except:
            s += "oh, dear"
        return s

    def get_course_details(self, soup):
        "Returns a dict of {courseid, area, title, descrip, prereqs}."
        try:
            area = CourseScraper.clean(soup('strong')[1].next_sibling)
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

        # match = re.match(
        #     r'\(([A-Z]+)\)',
        #     CourseScraper.clean(soup('strong')[1].findNext(text=True)))
        pretitle = soup.find(text=re.compile("Prerequisites"))
        descrdiv = soup.find('div', id='descr')

        title = CourseScraper.clean(soup('h2')[0].string)
        course_id = COURSE_URL_REGEX.search(
            soup.find(
                'a', href=COURSE_URL_REGEX)['href']).group('id')
        prereqs = CourseScraper.clean(
            pretitle.parent.findNextSibling(text=True)
        ) if pretitle is not None else ''  # broken spring 16 for many courses
        return {
            'courseid': course_id,
            'area': area,  # bwk: this was wrong[1:-1],
            'title': title,  # was [1]
            # 'descrip': clean(descrdiv.contents[0] if descrdiv else ''),
            'descrip': CourseScraper.clean(CourseScraper.flatten(descrdiv)),
            'prereqs': prereqs
        }

    def get_course_listings(self, soup):
        """Returns a list of {dept, number} dicts under which the course
        is listed."""
        listings = soup('strong')[1].string
        return [{
            'dept': match.group('dept'),
            'number': match.group('num')
        } for match in self.LISTING_REGEX.finditer(listings)]

    def get_course_profs(self, soup):
        """Returns a list of {uid, name} dicts for the professors teaching
        this course."""
        prof_links = soup('a', href=self.PROF_URL_REGEX)
        return [{
            'uid': self.PROF_URL_REGEX.search(link['href']).group('id'),
            'name': CourseScraper.clean(link.string)
        } for link in prof_links]

    def get_single_class(self, row):
        "Helper function to turn table rows into class tuples."
        cells = row('td')
        time = cells[2].string.split("-")
        bldg_link = cells[4].strong.a

        # <td><strong>Enrolled:</strong>0
        # <strong> Limit:</strong>11</td>
        enroll = ''
        limit = ''
        if cells[5] is not None:  # bwk
            enroll = cells[5].strong.nextSibling.string.strip()

            limit = cells[5].strong.nextSibling.nextSibling.nextSibling
            if limit is not None:
                limit = limit.string.strip()
            else:
                limit = "0"

        roomnum = bldg_link.nextSibling.string.replace('&nbsp;', ' ').strip()
        return {
            'classnum': cells[0].strong.string,
            'section': cells[1].strong.string,
            'days': re.sub(r'\s+', '', cells[3].strong.string),
            'starttime': time[0].strip(),
            'endtime': time[1].strip(),
            'bldg': bldg_link.string.strip(),
            'roomnum': roomnum,
            'enroll': enroll,  # bwk
            'limit': limit  # bwk
        }

    def get_course_classes(self, soup):
        """Returns a list of {classnum, days, starttime, endtime, bldg, roomnum}
        dicts for classes in this course."""
        class_rows = soup('tr')[
            1:]  # the first row is actually just column headings
        # This next bit tends to cause problems because the registrar includes
        # precepts and canceled classes. Having text in both 1st and 4th
        # columns (class number and day of the week) currently indicates a
        # valid class.
        return [
            self.get_single_class(row) for row in class_rows
            if row('td')[0].strong and row('td')[3].strong.string
        ]


class CourseProcessor(object):
    def __init__(self, root_path, verbose=False):
        root_path = root_path or ".."
        download_output = root_path + "/course_raw_html/"
        self.verbose = verbose
        self.downloader = CourseRegistrarDownloader(download_output, verbose)
        self.scraper = CourseScraper()

    def process_all(self, semester, year):
        self.downloader.fetch_all(semester, year)
        term_id = CourseRegistrarDownloader.get_term_id(semester, year)

        directory_path = self.downloader.get_output_path(semester, year)
        cur_files = os.listdir(directory_path)
        out_file_name = directory_path + '.json'
        out_file = open(out_file_name, 'w')
        out_file.write('[\n')
        for i, file_name in enumerate(cur_files):
            if self.verbose:
                print "Processing:", file_name
            file_path = '%s/%s' % (directory_path, file_name)
            f = open(file_path)
            page = f.read()
            page_data = self.scraper.scrape_page(page)
            page_data['termid'] = str(term_id)
            json.dump(page_data, out_file)
            if i < len(cur_files) - 1:
                out_file.write(',\n')
        out_file.write(']\n')


if __name__ == "__main__":
    if len(sys.argv) == 3:
        root_path = '/'.join(sys.argv[0].split('/')[:-1])
        processor = CourseProcessor(root_path, verbose=True)
        processor.process_all(sys.argv[1], int(sys.argv[2]))
    else:
        print "Must provide 2 arguments: semester and year. Ex:"
        print "python", sys.argv[0], "fall 2016"
        print "python", sys.argv[0], "spring 2017"
