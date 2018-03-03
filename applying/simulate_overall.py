from applying.models import Ministry,UserProfile
from applying.choices import ministry_name_choices,calculate_ministry_score



def simple_overall_simulate(series):
    general_admin_list = UserProfile.objects.filter(series_of_class=series).values('total_score','ranking','prefer_1st','prefer_2nd','prefer_3rd')
    general_admin_list = general_admin_list.order_by('ranking')
    general_admin_list = list(general_admin_list) # Convert queryset into list of dicts
    # intended result : [{... , 'allocated_ministry' : allocated_ministry}
    for item in general_admin_list:
        item['allocated_ministry'] = ''
    print(general_admin_list)

    ministry_general_list = list(Ministry.objects.filter(series_of_class=series).values('ministry_name','ministry_quota'))
    for item in ministry_general_list:
        item['count'] = 0 # intended result :[{'ministry_name':name, 'ministry_quota':quota, 'count':0}, ...]
    print(ministry_general_list)

    # allocate samugwans
    for samugwan in general_admin_list:
        first_ministry = next((item for item in ministry_general_list if item['ministry_name'] == samugwan['prefer_1st']))
        second_ministry = next((item for item in ministry_general_list if item['ministry_name'] == samugwan['prefer_2nd']))
        third_ministry = next((item for item in ministry_general_list if item['ministry_name'] == samugwan['prefer_3rd']))

        if first_ministry['ministry_quota'] > first_ministry['count']:
            first_ministry['count'] += 1
            samugwan['allocated_ministry'] = samugwan['prefer_1st']
        else:
            if second_ministry['ministry_quota'] > second_ministry['count']:
                second_ministry['count'] += 1
                samugwan['allocated_ministry'] = samugwan['prefer_2nd']
            else:
                if third_ministry['ministry_quota'] > third_ministry['count']:
                    third_ministry['count'] += 1
                    samugwan['allocated_ministry'] = samugwan['prefer_3rd']
                else:
                    samugwan['allocated_ministry'] = '잔여자'
        # Update Userprofile's Allocated_ministry
        # first, we have to convert samugwan['allocated_ministry'] into somewhat familiar. ex) 'MPVA' -> '국가보훈처'
        ministry_familiar = ''
        # exception handling
        if samugwan['allocated_ministry'] == '잔여자':
            ministry_familiar = '잔여자'
        else:
            for item in ministry_name_choices:
                if samugwan['allocated_ministry'] == item[0]:
                    ministry_familiar = item[1]


        UserProfile.objects.filter(series_of_class=series, ranking=samugwan['ranking']).update(allocated_ministry=ministry_familiar)



    # Rendering Tables for the result : lists of dictionary
    # [{'ministry_name': '감사원', 'allocated_samugwan' : [1, 4, 7, ]},{'ministry_name' : '공정위', []}...]
    # initialize list_of_dict
    list_of_dict = [] # surplus people....How?
    ministry_choices = list(ministry_name_choices)
    ministry_choices.append(('SUR','잔여자'))

    for name in ministry_choices:
        item={}
        item['ministry_name']=name[0]
        item['ministry_name_korean']=name[1]
        # exception handling for leftovers
        if name[0] == 'SUR':
            item['ministry_quota'] = ''
        else:
            item['ministry_quota'] = Ministry.objects.filter(ministry_name = name[0],series_of_class=series).values_list('ministry_quota', flat=True).get()
        item['allocated_samugwan'] = []
        list_of_dict.append(item)

# Allocating users
    for user in general_admin_list:
        for item in list_of_dict:
            if item['ministry_name'] == user['allocated_ministry']:
                item['allocated_samugwan'].append(user['ranking'])
    return list_of_dict

