from django import forms
from django.contrib.auth.models import User
from applying.models import UserProfile, Ministry


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('gender', 'passed_year', 'series_of_class', 'second_exam_score','nhi_score',)
        labels = {
                'gender': '성별',
                'passed_year': '합격연도',
                'series_of_class': '직렬',
                'second_exam_score': '2차 표준점수',
                'nhi_score': '연수원 표준점수'
        }


class UserApplyingForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('prefer_1st', 'other_score_1st', 'prefer_2nd', 'other_score_2nd', 'prefer_3rd', 'other_score_3rd')
        labels = {
            'prefer_1st': '1지망 부처',
            'other_score_1st': '1지망 부처 기타 점수',
            'prefer_2nd': '2지망 부처',
            'other_score_2nd': '2지망 부처 기타 점수',
            'prefer_3rd': '3지망 부처',
            'other_score_3rd': '3지망 부처 기타 점수'
        }


class MinistryApplyingResultForm(forms.ModelForm):

    class Meta:
        model = Ministry
        fields = ('ministry_name', 'series_of_class')
        labels = {
            'ministry_name': '부처',
            'series_of_class': '직렬'
        }


class UserOtherScoreForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('other_score_1st', 'other_score_2nd', 'other_score_3rd')