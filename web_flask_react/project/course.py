import cPickle as pickle
import re
import itertools
import json
from collections import defaultdict

distributions = ['LA', 'HA', 'SA', 'EM', 'STN', 'STL', 'QR', 'EC']


def safe_convert(x):
    try:
        return unicode(x, 'utf-8', errors='ignore')
    except (TypeError, UnicodeDecodeError) as e:
        return x


def minimizer(x, y):
    if (0 < len(x) < len(y)) or len(y) == 0:
        return safe_convert(x)
    return safe_convert(y)


def reconfigure_highlighting(term):
    if term.upper() in distributions:
        return ' %s ' % term
    return term


class Course(object):
    ratings_order = {
        'Overall Quality of the Course': 0,
        'Feedback for other students': 1,
        'Lectures': 2,
        'Papers, Reports, Problem Sets, Examinations': 3,
        'Readings': 4,
        'Classes': 5,
        'Precepts': 6,
        'Seminars': 7,
        'Laboratories': 8,
        'Studios': 9,
        'Ear Training': 10,
        'Language': 11,
        'Quality of Experience': 12,
        'Techniques & Strategies': 13,
    }

    term_ids = {
        '1114': "Spring '11",
        '1122': "Fall '11",
        '1124': "Spring '12",
        '1132': "Fall '12",
        '1134': "Spring '13",
        '1142': "Fall '13",
        '1144': "Spring '14",
        '1152': "Fall '14",
        '1154': "Spring '15",
        '1162': "Fall '15",
        '1164': "Spring '16",
        '1172': "Fall '16",
        '1174': "Spring '17"
    }

    def __init__(self, term_info_dict, planner, course_id):
        self.course_id = course_id
        self.term_info_dict = term_info_dict
        self.planner = planner
        for term_id in sorted(term_info_dict.keys(), reverse=True):
            if 'ratings' in self.term_info_dict[
                    term_id] and self.term_info_dict[term_id]['ratings']:
                self.default_term = term_id
                break
        else:
            self.default_term = sorted(term_info_dict.keys())[-1]

    def get_url_courseid(self):
        return '0' * (6 - len(self.course_id)) + self.course_id

    def get_default_term_text(self):
        return self.term_ids[self.default_term]

    def get_title(self, term_id=None):
        if term_id is None:
            term_id = self.default_term
        title = self.term_info_dict[term_id]['title']
        # if not title:
        #     title = self.term_info_dict[term_id]['COURSE_TITLE']
        return safe_convert(title)

    def get_area(self, term_id=None):
        if term_id is None:
            term_id = self.default_term
        area = self.term_info_dict[term_id]['area']
        return area

    def get_course_listings(self, term_id=None):
        if term_id is None:
            term_id = self.default_term
        listings = self.term_info_dict[term_id]['all_listings_string']
        # if not listings:
        #     listings = self.term_info_dict[term_id][
        #         'SUBJECT'] + ' ' + self.term_info_dict[term_id]['CATALOG_NBR']
        return listings

    def processed_course_listings(self, term_id=None):
        course_listings = self.get_course_listings(term_id)
        split_course_listings = course_listings.split(' | ')
        new_course_listings = ' '.join(split_course_listings[:2])
        if len(split_course_listings) > 2:
            new_course_listings += '...'
        return new_course_listings

    def get_list_of_course_nums(self, term_id=None):
        listings = self.get_course_listings(term_id).split(' | ')
        # course_num_list = []
        # for i in range(0, len(listings), 2):
        #     course_num_list.append(listings[i] + listings[i + 1])
        # return course_num_list
        return listings

    def get_professors(self, term_id=None):
        if term_id is None:
            term_id = self.default_term
        profs = self.term_info_dict[term_id]['prof_string']
        if not profs:
            profs = ''
        return profs
        # return unicode(profs, 'utf-8')

    # !!!!!!!!!!!

    def get_first_professor(self, profs):
        return safe_convert(profs.split('|')[0])

    def get_comments(self, term_id=None):
        if term_id is None:
            term_id = self.default_term
        if 'reviews' in self.term_info_dict[term_id]:
            return self.term_info_dict[term_id]['reviews'] or []
        else:
            return []

    def get_ratings_names(self):
        sorted_keys = sorted(
            [(spot, key) for key, spot in self.ratings_order.items()])
        return [key for spot, key in sorted_keys]

    def get_all_ratings(self, term_id=None):
        if term_id is None:
            term_id = self.default_term
        # ratings = [rating for name, rating in self.term_info_dict[term_id]['EVAL']]
        # import pdb; pdb.set_trace()
        ratings_dict = self.term_info_dict[term_id]['ratings']
        if len(ratings_dict) == 0:
            return [0] * len(self.ratings_order.keys())
        import pdb
        pdb.set_trace()
        ratings_list = []
        for key, spot in self.ratings_order.items():
            try:
                ratings_list.append((spot, ratings_dict[key]))
            except KeyError:
                pass
        sorted_ratings = sorted(ratings_list)
        ratings = [rating for spot, rating in sorted_ratings]
        return ratings

    def get_ratings_dict(self, term_id=None):
        if term_id is None:
            term_id = self.default_term
        if 'ratings' in self.term_info_dict[term_id]:
            ratings = self.term_info_dict[term_id]['ratings'] or {}
        else:
            ratings = {}
        return defaultdict(str, ratings)

    def get_ordered_ratings(self, term_id=None, as_json=True):
        color_list = [
            "#bcdf8a", "#f5f9ad", "#94c0cc", "#fad48b", "#ed7777", "#bcdf8a",
            "#f5f9ad"
        ]
        if term_id is None:
            term_id = self.default_term
        if 'ratings' in self.term_info_dict[term_id]:
            ratings = self.term_info_dict[term_id]['ratings']
            if isinstance(ratings, dict):
                order = []
                for cat, rat in ratings.items():
                    order.append((self.ratings_order[cat], cat, rat))
                result = [(tup[1], tup[2], "color: %s" % color_list[i])
                          for i, tup in enumerate(sorted(order))]
                if as_json:
                    return json.dumps(result)
                return result
        return []

    def get_most_recent_overall_rating(self):
        course_dict = self.term_info_dict[self.default_term]
        if 'ratings' in course_dict and course_dict['ratings']:
            try:
                # return ratings_list[self.ratings_order['Overall Quality of the Course']][1]
                return course_dict['ratings']['Overall Quality of the Course']
            except (KeyError, IndexError) as e:
                print e
                # import pdb; pdb.set_trace()
                return 0
        else:
            return 0

    def get_highlighted_text(self, terms):
        if len(terms) == 0:
            return ''
        terms = [reconfigure_highlighting(term) for term in terms]
        top_num = -1
        top_comment = ''
        second_num = -1
        second_comment = ''
        for term_id, info_dict in self.term_info_dict.items():
            reviews = info_dict['reviews'] if 'reviews' in info_dict else None
            reviews = reviews or [
                info_dict['title'], info_dict['descrip'], info_dict['area']
            ]
            for comment in reviews:
                num_terms = 0
                for term in terms:
                    if term.lower() in safe_convert(comment.lower()):
                        num_terms += 1
                if num_terms > top_num:
                    second_num = top_num
                    second_comment = top_comment
                    top_num = num_terms
                    top_comment = comment
                elif num_terms > second_num:
                    second_num = num_terms
                    second_comment = comment
        if top_comment == second_comment:
            second_comment = ''

        if top_comment == '' or second_comment == '':
            for term_id, info_dict in self.term_info_dict.items():
                reviews = info_dict[
                    'reviews'] if 'reviews' in info_dict else None
                reviews = reviews or []
                for comment in reviews:
                    if top_comment == '':
                        top_comment = comment
                    elif second_comment == '':
                        second_comment = comment
                    else:
                        break

        for term in terms:
            top_comment = safe_convert(top_comment).replace(
                term, '<u><b>' + term + '</b></u>')
            top_comment = safe_convert(top_comment).replace(
                term.upper(), '<u><b>' + term.upper() + '</b></u>')
            top_comment = safe_convert(top_comment).replace(
                term.lower(), '<u><b>' + term.lower() + '</b></u>')
            second_comment = safe_convert(second_comment).replace(
                term, '<u><b>' + term + '</b></u>')
            second_comment = safe_convert(second_comment).replace(
                term.upper(), '<u><b>' + term.upper() + '</b></u>')
            second_comment = safe_convert(second_comment).replace(
                term.lower(), '<u><b>' + term.lower() + '</b></u>')
        return safe_convert(top_comment), safe_convert(second_comment)
        # doc =  self.term_info_dict[self.default_term]['document'].lower()
        # results = []
        # for term_list in itertools.permutations(terms):
        # 	pattern = ' .*? '.join(terms)
        # 	pattern = '.{0,20}' + pattern + '.{0,20}'
        # 	results.extend(re.findall(pattern, doc))
        # # import pdb; pdb.set_trace()
        # if len(results) > 0:
        # 	return '...' + reduce(minimizer, results) + '...'
        # else:
        # 	# import pdb; pdb.set_trace()
        # 	new_term_lists = [list(terms) for _ in range(len(terms))]
        # 	for i,term in enumerate(terms):
        # 		new_term_lists[i].remove(term)
        # 	new_results = [self.get_highlighted_text(new_term_lists[i]) for i in range(len(terms))]
        # 	# import pdb; pdb.set_trace()
        # 	return reduce(minimizer, new_results)


class CourseRenderer(object):
    def __init__(self, course_info_dict, planner):
        # self.course_info_dict = pickle.load(open(filename, 'rb'))
        self.course_info_dict = course_info_dict
        self.planner = planner

    def get_course(self, course_id):
        return Course(self.course_info_dict[course_id], self.planner,
                      course_id)
