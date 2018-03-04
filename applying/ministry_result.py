from applying.models import UserProfile, Ministry
import applying.choices
from operator import itemgetter
from decimal import Decimal

def result_ministry_applicants(ministry_name, series_of_class):
    applied_samugwan_list_test = getattr(
        Ministry.objects.get(ministry_name=ministry_name, series_of_class=series_of_class),
        'applied_samugwan')

    dict_list_test = []
    for key, value in applied_samugwan_list_test.items():
        dict_test = {}
        dict_test['name'] = key
        # convert into familiar names
        if value[0] == 'female':
            dict_test['gender'] = '여성'
        if value[0] == 'male':
            dict_test['gender'] = '남성'
        dict_test['total_score'] = value[1]
        dict_test['total_rank'] = value[2]
        dict_test['preference'] = value[3]
        dict_test['other_score'] = value[4]
        dict_test['ministry_score'] = value[5]
        dict_list_test.append(dict_test)

    # Sorting, must be reversed(descending order)
    dict_list_test = sorted(dict_list_test, key=itemgetter('ministry_score'), reverse=True)
    for item in dict_list_test:
        item['rank_by_ministry'] = dict_list_test.index(item) + 1

    return dict_list_test

def result_ministry_stats(ministry_name, series_of_class):
    # Make a dictionary to show statistics about ministry
    dict_stat = {}
    for name in applying.choices.ministry_name_choices:
        if name[0] == ministry_name:
            dict_stat['name'] = name[1]
    if series_of_class == 'general_admin':
        dict_stat['series_of_class'] = '일반행정'
    else:
        dict_stat['series_of_class'] = '재경'
    dict_stat['ministry_quota'] = getattr(
        Ministry.objects.get(ministry_name=ministry_name, series_of_class=series_of_class),
        'ministry_quota')
    dict_stat['second_exam_ratio'] = getattr(
        Ministry.objects.get(ministry_name=ministry_name, series_of_class=series_of_class),
        'second_exam_ratio')
    dict_stat['nhi_score_ratio'] = getattr(
        Ministry.objects.get(ministry_name=ministry_name, series_of_class=series_of_class),
        'NHI_score_ratio')
    dict_stat['number_of_applicants'] = len(getattr(
        Ministry.objects.get(ministry_name=ministry_name, series_of_class=series_of_class),
        'applied_samugwan'))
    dict_stat['competition_rate_overall'] = Decimal(dict_stat['ministry_quota'] / dict_stat['number_of_applicants'])
    dict_stat['competition_rate_1st'] = Decimal(
        UserProfile.objects.filter(prefer_1st=ministry_name).count() / dict_stat['number_of_applicants'])

    return dict_stat

