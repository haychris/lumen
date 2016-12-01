import os
import sys

import urllib2
import dryscrape

from unidecode import unidecode
from bs4 import BeautifulSoup
import re
import json

REGISTRAR_URL_PREFIX = "http://registrar.princeton.edu/course-offerings/"
COURSE_URL_TEMPLATE = REGISTRAR_URL_PREFIX + "course_details.xml?courseid={courseid}&term={term}"
COURSE_URL_REGEX = re.compile(r'courseid=(?P<id>\d+)')
COURSE_RATINGS_TEMPLATE = "https://reg-captiva.princeton.edu/chart/index.php?terminfo={term}&courseinfo={courseid}"


class CourseRegistrarDownloader(object):
    COURSE_LISTINGS_URL_TEMPLATE = REGISTRAR_URL_PREFIX + "search_results.xml?term={term}"
    OUTPUT_TYPE_LOOKUP = {
        "registrar": "course_raw_html/",
        "reviews": "course_reviews_raw_html/",
        "processed": "course_processed_data/"
    }

    def __init__(self,
                 root_output_path,
                 registrar_url_template,
                 reviews_url_template,
                 verbose=False):
        self.root_output_path = root_output_path
        self.verbose = verbose
        self.course_ids = None
        self.url_templates = {
            "registrar": registrar_url_template,
            "reviews": reviews_url_template
        }

    def get_output_path(self, semester, year, output_type):
        sem = semester.lower()
        assert (sem == "fall" or sem == "spring")
        assert (year > 2000)
        assert (output_type == "registrar" or output_type == "reviews" or
                output_type == "processed")
        path = self.root_output_path + self.OUTPUT_TYPE_LOOKUP[output_type]
        return "{0}{1}_{2}".format(path, sem, year)

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
        if self.course_ids is not None:
            return self.course_ids

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

        self.course_ids = set(courseids)
        return self.course_ids

    def fetch_all_registrar(self, semester, year, redownload=False):
        self.__fetch_all(semester, year, "registrar",
                         self.__download_dryscrape, redownload)

    def fetch_all_reviews(self, semester, year, redownload=False):
        self.__fetch_all(semester, year, "reviews", self.__download_dryscrape,
                         redownload)

    def __download_urllib2(self, url):
        return urllib2.urlopen(url).read()

    def __download_dryscrape(self, url):
        """Downloads url using dryscrape, which handles unicode and javascript
        natively whereas urllib2 does not. """
        session = dryscrape.Session()
        session.visit(url)
        return session.body()

    def __fetch_all(self,
                    semester,
                    year,
                    output_type,
                    downloader,
                    redownload=False):
        """Fetches all html pages in the registrar/course reviews for the
        given semester and year, and stores the html files in a directory named
        by get_output_path(semester, year, output_type). Option to redownload
        and overwrite existing."""
        term_id = CourseRegistrarDownloader.get_term_id(semester, year)
        courseids = self.get_course_ids(semester, year)
        directory_path = self.get_output_path(semester, year, output_type)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        cur_files = os.listdir(directory_path)
        if self.verbose:
            print '%d of %d files already indexed' % (len(cur_files),
                                                      len(courseids))
        num_to_process = len(courseids) - len(cur_files)
        count = 0
        for i, courseid in enumerate(courseids):
            if '{0}.html'.format(courseid) not in cur_files or redownload:
                if self.verbose:
                    print 'Retrieving html %d / %d, index: %d, courseid:%s' % (
                        count, num_to_process, i, courseid)
                url_template = self.url_templates[output_type]
                course_url = url_template.format(
                    term=term_id, courseid=courseid)
                course_page = downloader(course_url)
                file_path = '{directory_path}/{courseid}.html'.format(
                    directory_path=directory_path, courseid=courseid)

                try:
                    f = open(file_path, 'w')
                    f.write(unidecode(course_page))
                    f.close()
                    count += 1
                except UnicodeDecodeError as e:
                    print course_page
                    raise e


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
        if re.match(r'^\((LA|SA|HA|EM|EC|QR|STN|STL|W)\)$', area):
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
            'endtime': time[1].strip() if len(time) >= 2 else None,
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


class CourseReviewsScraper(object):
    def __init__(self):
        pass

    def scrape_page(self, page, term):
        soup = BeautifulSoup(page, 'lxml')
        term_shown = self.get_term_shown(soup)
        if term_shown is None:
            # hacky way for classes without professors listed
            if 'terminfo={0}'.format(term) in page:
                term_shown = term
        if term_shown != term:
            reviews, ratings = None, None
        else:
            reviews = self.get_reviews(soup)
            ratings = self.get_ratings(soup)
        return {"reviews": reviews, "ratings": ratings}

    def get_term_shown(self, soup):
        try:
            instructor_lookup = str(soup(href=re.compile("instructor.php"))[0])
            term_shown = int(instructor_lookup.split('term=')[1].split('&')[0])
            return term_shown
        except:
            return None

    def get_reviews(self, soup):
        underlined = soup('u')
        comment_start = None
        for el in underlined:
            if 'Student Comments' in el:
                comment_start = el.parent.parent.parent.next_sibling
                break

        if comment_start is None:
            return None
        return [comment.string for comment in comment_start.next_siblings]

    def get_ratings(self, soup):
        charts = soup(id='chart')
        if not charts:
            return None, None
        semp = charts[0]('tspan')[6].parent

        categories = []
        cur = semp
        while cur is not None and cur.name != 'rect':
            categories.append(cur('tspan')[0].string)
            cur = cur.next_sibling

        # graph is empty
        if cur is None:
            return None, None

        ratings = []
        cur = cur.next_sibling  # skip holder rect
        for category in categories:
            txt = cur.next_sibling.string
            ratings.append(float(txt))
            cur = cur.next_sibling.next_sibling
        ratings = list(reversed(ratings))  # flip order to match categories

        return categories, ratings


class CourseProcessor(object):
    def __init__(self, root_path, verbose=False, fetch_reviews=False):
        root_path = root_path or ".."
        download_output = root_path + "/"
        self.verbose = verbose
        self.downloader = CourseRegistrarDownloader(
            download_output, COURSE_URL_TEMPLATE, COURSE_RATINGS_TEMPLATE,
            verbose)
        self.course_scraper = CourseScraper()
        self.course_review_scraper = CourseReviewsScraper()
        self.fetch_reviews = fetch_reviews

    def process_all(self, semester, year):
        self.downloader.fetch_all_registrar(semester, year, False)
        if self.fetch_reviews:
            self.downloader.fetch_all_reviews(semester, year, False)
        term_id = CourseRegistrarDownloader.get_term_id(semester, year)

        registrar_path = self.downloader.get_output_path(semester, year,
                                                         "registrar")
        reviews_path = self.downloader.get_output_path(semester, year,
                                                       "reviews")
        processed_path = self.downloader.get_output_path(semester, year,
                                                         "processed")

        cur_files = os.listdir(registrar_path)
        out_file = open(processed_path + '.json', 'w')
        out_file.write('[\n')
        for i, file_name in enumerate(cur_files):
            if self.verbose:
                print "Processing:", file_name
            course_page = open('%s/%s' % (registrar_path, file_name)).read()
            course_page_data = self.course_scraper.scrape_page(course_page)
            course_page_data['termid'] = str(term_id)

            if self.fetch_reviews:
                review_page = open('%s/%s' % (reviews_path, file_name)).read()
                review_page_data = self.course_review_scraper.scrape_page(
                    review_page, term_id)
                course_page_data.update(review_page_data)

            json.dump(course_page_data, out_file)
            if i < len(cur_files) - 1:
                out_file.write(',\n')
        out_file.write(']\n')


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        root_path = '/'.join(sys.argv[0].split('/')[:-1])
        if len(sys.argv) > 3:
            fetch_reviews = sys.argv[3].lower() == 'false'
        else:
            fetch_reviews = False
        processor = CourseProcessor(
            root_path, verbose=True, fetch_reviews=not fetch_reviews)
        processor.process_all(sys.argv[1], int(sys.argv[2]))
    else:
        print "Must provide at least 2 arguments: semester and year. Ex:"
        print "python", sys.argv[0], "fall 2016"
        print "python", sys.argv[0], "spring 2017"
