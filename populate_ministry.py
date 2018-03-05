import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','project_samugwan.settings')
import copy

import django
django.setup()
from applying.models import UserProfile, Ministry


def populate():
    # make a dictionaries of min_name and series_of_class
    ministry_name_choices = (
        ('BAI', '감사원'), ('MOEL', '고용노동부'), ('KFTC', '공정거래위원회'), ('MSIT', '과학기술정보통신부'),
        ('KCS', '관세청'), ('MOE', '교육부'), ('MPVA', '국가보훈처'), ('NHRC', '국가인권위원회'), ('OPC', '국무총리실'),
        ('ACRC', '국민권익위원회'), ('MND', '국방부'), ('NTS', '국세청'), ('MOLIT', '국토교통부'), ('FSC', '금융위원회'), ('MOSF', '기획재정부'),
        ('MAFRA', '농림축산식품부'), ('CHA', '문화재청'), ('MCST', '문화체육관광부'), ('KCC', '방송통신위원회'),
        ('DAPA', '방위사업청'), ('MOLEG', '법제처'), ('MMA', '병무청'), ('MOHW', '보건복지부'), ('KFS', '산림청'),
        ('MOTIE', '산업통상자원부'), ('SDIA', '새만금개발청'), ('MFDS', '식품의약품안전처'), ('MOGEF', '여성가족부'),
        ('MPM', '인사혁신처'), ('PPS', '조달청'), ('MSS', '중소벤처기업부'), ('NEC', '중앙선거관리위원회'), ('KOSTAT', '통계청'),
        ('MOU', '통일부'), ('KIPO', '특허청'), ('MOF', '해양수산부'), ('MOIS', '행정안전부'), ('NAACC', '행정중심복합도시건설청'),
        ('ME', '환경부')
    )

    # nested list : [name, general_admin_quota, econ_admin_quota, second_exam_ratio, NHI_score_ratio]
    # ratios are all correct(need to be checked), but quotas to be revised
    ministry_list = [['BAI', 2, 2, 3, 1], ['MOEL', 12, 0, 2.5, 1.5], ['KFTC', 0, 8, 5, 3], ['MSIT', 7, 3, 3.5, 3.5],
                     ['KCS', 0, 3, 3, 1], ['MOE', 4, 1, 2.5, 2.5], ['MPVA', 3, 0, 3, 3], ['NHRC', 3, 0, 3, 2], ['OPC', 9, 2, 4, 1],
                     ['ACRC', 2, 0, 2.5, 2.5], ['MND', 3, 1, 3, 2], ['NTS', 3, 10, 3, 2.5], ['MOLIT', 3, 4, 3, 3], ['FSC', 0, 6, 2.5, 2.5], ['MOSF', 5, 24, 4, 2],
                     ['MAFRA', 11, 1, 3, 3], ['CHA', 1, 0, 3, 2], ['MCST', 7, 0, 3, 2], ['KCC', 2, 0, 3, 2],
                     ['DAPA', 5, 0, 2.5, 2.5], ['MOLEG', 1, 0, 2.5, 2.5], ['MMA', 1, 0, 4, 2], ['MOHW', 11, 2, 2.5, 2.5], ['KFS', 1, 0, 2.5, 2.5],
                     ['MOTIE', 3, 5, 3, 2], ['SDIA', 1, 0, 3, 3], ['MFDS', 2, 0, 2.5, 1.5], ['MOGEF', 2, 0, 1.5, 2.5],
                     ['MPM', 0, 0, 4, 3], ['PPS', 1, 0, 4.5, 3], ['MSS', 3, 3, 3, 3], ['NEC', 2, 0, 2, 2], ['KOSTAT', 0, 2, 2, 2],
                     ['MOU', 5, 0, 2, 2], ['KIPO', 3, 0, 4.5, 2.5], ['MOF', 7, 0, 2.5, 2.5], ['MOIS', 8, 2, 2.5, 2.5], ['NAACC', 1, 0, 2.5, 2.5],
                     ['ME', 5, 0, 3, 2]
                     ]

    # copy by value(not reference)
    ministry_list_admin = copy.deepcopy(ministry_list)
    # ministry_list_admin = [name, general_admin_quota, sec_ratio, NHI_ratio]
    for item in ministry_list_admin:
        del item[2]
        add_ministry_general(item[0], item[1], item[2], item[3])
        print('adding  ' + str(item) + ' in general admin')

    ministry_list_econ = copy.deepcopy(ministry_list)
    print(ministry_list_econ)
    for item in ministry_list_econ:
        del item[1]
        add_ministry_econ(item[0], item[1], item[2], item[3])
        print('adding  ' + str(item) + ' in econ admin')


def add_ministry_general(name, quota, second_exam_ratio, NHI_score_ratio):
    min_admin = Ministry.objects.get_or_create(ministry_name=name, series_of_class = 'general_admin')[0]
    min_admin.ministry_quota = quota
    min_admin.second_exam_ratio = second_exam_ratio
    min_admin.NHI_score_ratio = NHI_score_ratio

    min_admin.save()
    return min_admin

def add_ministry_econ(name, quota, second_exam_ratio, NHI_score_ratio):
    min_econ = Ministry.objects.get_or_create(ministry_name=name, series_of_class = 'econ_admin')[0]
    min_econ.ministry_quota = quota
    min_econ.second_exam_ratio = second_exam_ratio
    min_econ.NHI_score_ratio = NHI_score_ratio

    min_econ.save()
    return min_econ

# Start Execution here!
if __name__ == '__main__' :
    print("Starting Ministry Populating Script...")
    populate()

