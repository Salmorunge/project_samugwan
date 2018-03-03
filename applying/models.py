from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from applying.choices import ministry_name_choices
from jsonfield import JSONField
# Create your models here.


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include
    # second_exam_score, nhi_score, other_score, interview_score(not to be used..maybe), total_score
    # They are all raw scores, so added a _raw tag

    gender_choices = (
        ('female', '여성'),
        ('male', '남성'),
    )
    gender = models.CharField(
        max_length=6,
        choices=gender_choices,
        default='female',
    )

    passed_year_choices = (
        ('year_before', '2014년 이전'),
        ('year_2015', '2015년'),
        ('year_2016', '2016년'),
    )
    passed_year = models.CharField(
        max_length=20,
        choices=passed_year_choices,
        default='year_2016',
    )

    series_of_class_choices = (
        ('general_admin', '일반행정'),
        ('econ_admin', '재경'),
        ('others_admin', '기타직렬'),
    )
    series_of_class = models.CharField(
        max_length=20,
        choices=series_of_class_choices,
        default='general_admin',
    )

    # normalized and total score, ranking
    second_exam_score = models.FloatField(default=0)
    nhi_score = models.FloatField(default=0)

    # other_score needed to be diversed between ministries
    other_score_1st = models.FloatField(default=0)
    other_score_2nd = models.FloatField(default=0)
    other_score_3rd = models.FloatField(default=0)


    total_score = models.FloatField(default=0)
    ranking = models.IntegerField(default=0)

    # preferred ministry(import from Ministry Model)
    prefer_1st = models.CharField(choices=ministry_name_choices, max_length=20, default='')
    prefer_2nd = models.CharField(choices=ministry_name_choices, max_length=20, default='')
    prefer_3rd = models.CharField(choices=ministry_name_choices, max_length=20, default='')

    allocated_ministry = models.CharField(max_length=20)

    # Constructor
    def __str__(self):
        return self.user.username

# New class, Ministry, which actually used for applying.
# It contains actually applied users for each ministry object.
class Ministry(models.Model):

    ministry_name = models.CharField(
        max_length=20,
        choices=ministry_name_choices,
    )

    ministry_quota = models.IntegerField(default=0)

    series_of_class_choices = (
        ('general_admin', '일반행정'),
        ('econ_admin', '재경'),
        ('others_admin', '기타직렬'),
    )

    series_of_class = models.CharField(
        max_length=20,
        choices=series_of_class_choices,
    )


    # applied samugwan. linked at view//
    # dictionary form : applied_samugwan.{'prefer_1st_user': [username, gender, total_score_(by ministry criteria), rank by total score, rank by ministry criteria]
    # Testing JSONField
    applied_samugwan = JSONField(default=dict)

    number_of_applicants = models.IntegerField(default=0)

    second_exam_ratio = models.FloatField(default=0)

    NHI_score_ratio = models.FloatField(default=0)


    def __str__(self):
        return self.ministry_name


