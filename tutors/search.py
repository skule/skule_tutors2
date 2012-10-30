__author__ = 'Oliver'
from models import Tutor
import collections
import random

class NoSearchTerms(Exception):
    pass


def remove_values_from_list(the_list, val):
    return [ value for value in the_list if value.lower() not in val and len(value) >= 2 ]


def strSearchTutors(search_terms = ''):
    """
    This function takes in a string, and returns a list.

    The list consists of Tutor, ordered by how close they match the inputted string
    """

    if not search_terms:
        raise NoSearchTerms

    search_terms = remove_values_from_list(search_terms.split(' '),
                                           [ 'and', 'or', '+', '\'', '\t', '\"' ])

    result_list = [ ]

    # result of matching courses by course_code
    for term in search_terms:
        tutor_set = Tutor.objects.filter(taught_courses__course_code__iexact = term)
        for tutor in tutor_set:
            result_list.append(tutor)
            # matches for course name
        if not tutor_set:
            tutor_set = Tutor.objects.filter(taught_courses__name__icontains = term)
            for tutor in tutor_set:
                result_list.append(tutor)
                # result of matching names
        if not tutor_set:
            tutor_set = Tutor.objects.filter(name__icontains = term)
            for tutor in tutor_set:
                result_list.append(tutor)

    # List the tutor by how many search terms they match
    result_counted = collections.Counter(result_list)

    result_by_count = {}
    for tutor, count in dict(result_counted).iteritems():
        if count in result_by_count:
            result_by_count[ count ].append(tutor)
        else:
            result_by_count[ count ] = [ tutor ]

    result = [ ]
    while result_by_count:
        max_count_result = result_by_count[ max(result_by_count.keys()) ]
        random.shuffle(max_count_result)
        result += max_count_result
        del result_by_count[ max(result_by_count.keys()) ]

    return result