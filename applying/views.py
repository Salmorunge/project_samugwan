from django.shortcuts import render
from applying.forms import UserProfileForm, UserApplyingForm, MinistryApplyingResultForm
from applying.models import UserProfile, Ministry
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig
from applying.tables import ResultTable, AppliedDictionaryTable, ResultByMinistryTable, ApplyingSimulationTable
from applying.choices import calculate_ministry_score
import applying.choices
from operator import itemgetter
from applying.simulate_overall import simple_overall_simulate
from decimal import Decimal
from applying.ministry_result import result_ministry_applicants, result_ministry_stats

# Create your views here.
def index(request):
    list=[]
    number_general = UserProfile.objects.filter(series_of_class='general_admin').count()
    list.append(number_general)
    number_econ = UserProfile.objects.filter(series_of_class='econ_admin').count()
    list.append(number_econ)
    return render(request, 'applying/index.html', {'list': list})

@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            # Trying to calculate normalized data and rankings

            # First, try to get normalized scores for second exam
            # should be categorized with passed_year and series_of_class
            # Get average and standard deviation per each passed_year and series_of_class
            # Updates statistics, too
            # We use Decimal to avoid precision problems with float type.

            total_score_deci = Decimal(user_profile.second_exam_score + user_profile.nhi_score)
            total_score_deci = round(total_score_deci,2)
            user_profile.total_score = float(total_score_deci)
            user_profile.save()

            # Finally, we should calculate a rank of the specific user in each series of class(IMPORTANT!!!).
            raw_list = UserProfile.objects.filter(series_of_class=user_profile.series_of_class).order_by("-total_score")
            for i in range(UserProfile.objects.filter(series_of_class=user_profile.series_of_class).count()):
                UserProfile.objects.filter(user=raw_list[i].user).update(ranking=i+1)

            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form': form}

    return render(request, 'applying/profile_registration.html', context_dict)


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    neededform = {'gender': userprofile.gender,
                  'passed_year': userprofile.passed_year,
                  'series_of_class': userprofile.series_of_class,
                  'second_exam_score': userprofile.second_exam_score,
                  'nhi_score': userprofile.nhi_score,
                  }

    form = UserProfileForm(neededform)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)

            # Update other_score and total_score
            total_score_pre = Decimal(userprofile.second_exam_score + userprofile.nhi_score)
            total_score_pre = round(total_score_pre,2)
            userprofile.total_score = float(total_score_pre)
            userprofile.save()

            # Next, calculate a rank of the specific user.
            raw_list = UserProfile.objects.filter(series_of_class=userprofile.series_of_class).order_by("-total_score")
            for i in range(UserProfile.objects.filter(series_of_class=userprofile.series_of_class).count()): # i str
                UserProfile.objects.filter(user=raw_list[i].user).update(ranking=i+1)

            # Finally, update objects of ministry(we should update rank)


            return redirect('profile', user.username)
        else:
            print(form.errors)

    return render(request, 'applying/profile.html',
                  {'userprofile': userprofile, 'selecteduser': user, 'form': form})


@login_required
def apply(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    applyingform = {'1순위 지망부처' : userprofile.prefer_1st,
                    '2순위 지망부처' : userprofile.prefer_2nd,
                    '3순위 지망부처' : userprofile.prefer_3rd
                  }

    form = UserApplyingForm(applyingform)

    if request.method == 'POST':
        # Before update userprofile, 'clear' the previous result(IMPORTANT)
        ministry_before_1st = Ministry.objects.get_or_create(ministry_name=userprofile.prefer_1st, series_of_class=userprofile.series_of_class)[0]
        if username in ministry_before_1st.applied_samugwan:
            del ministry_before_1st.applied_samugwan[username]
        ministry_before_1st.save()

        ministry_before_2nd = Ministry.objects.get_or_create(ministry_name=userprofile.prefer_2nd, series_of_class=userprofile.series_of_class)[0]
        if username in ministry_before_2nd.applied_samugwan:
            del ministry_before_2nd.applied_samugwan[username]
        ministry_before_2nd.save()

        ministry_before_3rd = Ministry.objects.get_or_create(ministry_name=userprofile.prefer_3rd, series_of_class=userprofile.series_of_class)[0]
        if username in ministry_before_3rd.applied_samugwan:
            del ministry_before_3rd.applied_samugwan[username]
        ministry_before_3rd.save()

        form = UserApplyingForm(request.POST, instance=userprofile)
        if form.is_valid():
            print(userprofile.user_id)
            form.save(commit=True)
            # Trying to calculate normalized data and rankings
            userprofile.save()


            # Update each Ministrys
            ministry_1st = Ministry.objects.get_or_create(ministry_name=userprofile.prefer_1st, series_of_class=userprofile.series_of_class)[0]
            # Compute Total Score By Ministry's Criteria
            ministry_1st_score = calculate_ministry_score(userprofile,ministry_1st, userprofile.other_score_1st)

            # dictionary form : applied_samugwan.{'prefer_1st_user': [gender, total_score_(by ministry criteria),
            #                                                           rank by total score, rank by ministry criteria]}
            ministry_1st.applied_samugwan.update({username:[userprofile.gender,userprofile.total_score,userprofile.ranking, 1, userprofile.other_score_1st, ministry_1st_score]})
            ministry_1st.save()

            # Update 2nd Min.
            ministry_2nd = Ministry.objects.get_or_create(ministry_name=userprofile.prefer_2nd, series_of_class=userprofile.series_of_class)[0]
            ministry_2nd_score = calculate_ministry_score(userprofile, ministry_2nd, userprofile.other_score_2nd)
            ministry_2nd.applied_samugwan.update({username:[userprofile.gender,userprofile.total_score,userprofile.ranking, 2, userprofile.other_score_2nd, ministry_2nd_score]})
            ministry_2nd.save()

            # Update 3rd Min.
            ministry_3rd = Ministry.objects.get_or_create(ministry_name=userprofile.prefer_3rd, series_of_class=userprofile.series_of_class)[0]
            ministry_3rd_score = calculate_ministry_score(userprofile, ministry_3rd, userprofile.other_score_3rd)
            ministry_3rd.applied_samugwan.update({username:[userprofile.gender,userprofile.total_score,userprofile.ranking, 3, userprofile.other_score_3rd, ministry_3rd_score]})
            ministry_3rd.save()

            return redirect('apply', user.username)
        else:
            print(form.errors)

    return render(request, 'applying/apply.html',
                  {'userprofile': userprofile, 'selecteduser': user, 'form1': form})

def result_general_admin(request):
    table = ResultTable(UserProfile.objects.filter(series_of_class='general_admin'))
    RequestConfig(request, paginate=False).configure(table)
    return render(request, 'applying/result_general.html', {'table':table})

def result_econ_admin(request):
    table = ResultTable(UserProfile.objects.filter(series_of_class='econ_admin'))
    RequestConfig(request, paginate=False).configure(table)
    return render(request, 'applying/result_econ.html', {'table':table})


# a function to render applying result_by_ministry into a table
def result_by_ministry(request):
    form = MinistryApplyingResultForm()
    if request.method == 'POST':
        form = MinistryApplyingResultForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            data = form.cleaned_data
            data_ministry_name = data.get('ministry_name')
            data_series_of_class = data.get('series_of_class')

            # make a new list of dictionaries for table
            applied_samugwan_list_test = getattr(
                Ministry.objects.get(ministry_name=data_ministry_name, series_of_class=data_series_of_class),
                'applied_samugwan')
            print(applied_samugwan_list_test)

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
                # used to update user_rankings realtime
                try:
                    selected_user = User.objects.get(username=key)
                    selected_rank = UserProfile.objects.get(user=selected_user).ranking
                    dict_test['total_rank'] = selected_rank
                except:
                    dict_test['total_rank'] = 0

                dict_test['preference'] = value[3]
                dict_test['other_score'] = value[4]
                dict_test['ministry_score'] = value[5]
                dict_list_test.append(dict_test)

            # Sorting, must be reversed(descending order)
            dict_list_test = sorted(dict_list_test, key=itemgetter('ministry_score'), reverse=True)
            for item in dict_list_test:
                item['rank_by_ministry'] = dict_list_test.index(item) + 1
            print(dict_list_test)

            # Make a dictionary to show statistics about ministry
            dict_stat = {}
            dict_stat['name'] = data_ministry_name
            dict_stat['series_of_class'] = data_series_of_class
            dict_stat['ministry_quota'] = getattr(
                Ministry.objects.get(ministry_name=data_ministry_name, series_of_class=data_series_of_class),
                'ministry_quota')
            dict_stat['second_exam_ratio'] = getattr(
                Ministry.objects.get(ministry_name=data_ministry_name, series_of_class=data_series_of_class),
                'second_exam_ratio')
            dict_stat['nhi_score_ratio'] = getattr(
                Ministry.objects.get(ministry_name=data_ministry_name, series_of_class=data_series_of_class),
                'NHI_score_ratio')
            dict_stat['number_of_applicants'] = len(dict_list_test)

            # Exception Handling
            count = UserProfile.objects.filter(prefer_1st= data_ministry_name, series_of_class= data_series_of_class).count()
            if dict_stat['ministry_quota'] == 0:
                dict_stat['competition_rate_overall'] = 0
                dict_stat['competition_rate_1st'] = 0
            else:
                dict_stat['competition_rate_overall'] = round(Decimal(dict_stat['number_of_applicants']/dict_stat['ministry_quota']),2)
                dict_stat['competition_rate_1st'] = round(Decimal(count/dict_stat['ministry_quota']),2)

            # Render table
            table = ResultByMinistryTable(dict_list_test)
            RequestConfig(request).configure(table)
            return render(request, 'applying/result2.html',
                          {'list': dict_list_test, 'form': form, 'table' : table, 'dict': dict_stat})

        else:
            print(form.errors)

    #'list': applied_samugwan_list,
    return render(request, 'applying/result2.html',
                  {'form': form})

# a function to render simulation for result1(overall)
def simulate_overall_general_admin(request):

    table = ApplyingSimulationTable(simple_overall_simulate('general_admin'))
    RequestConfig(request, paginate=False).configure(table)

    return render(request, 'applying/result3_general.html', {'table' : table})

def simulate_overall_econ_admin(request):

    table = ApplyingSimulationTable(simple_overall_simulate('econ_admin'))
    RequestConfig(request, paginate=False).configure(table)

    return render(request, 'applying/result3_econ.html', {'table' : table})

# a view to show indivisual's applied ministry result

@login_required
def result_ministry_user(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]

    dict_stats_1st = result_ministry_stats(userprofile.prefer_1st, userprofile.series_of_class)
    list_1st = result_ministry_applicants(userprofile.prefer_1st, userprofile.series_of_class)

    dict_stats_2nd = result_ministry_stats(userprofile.prefer_2nd, userprofile.series_of_class)
    list_2nd= result_ministry_applicants(userprofile.prefer_2nd, userprofile.series_of_class)

    dict_stats_3rd = result_ministry_stats(userprofile.prefer_3rd, userprofile.series_of_class)
    list_3rd = result_ministry_applicants(userprofile.prefer_3rd, userprofile.series_of_class)

    return render(request, 'applying/result4.html', {'selecteduser': user, 'profile' : userprofile,
                                                     'list1': list_1st, 'dict1': dict_stats_1st,
                                                     'list2': list_2nd, 'dict2': dict_stats_2nd,
                                                     'list3': list_3rd, 'dict3': dict_stats_3rd,})
