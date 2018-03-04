import django_tables2 as tables
from applying.models import Ministry, UserProfile


class ResultTable(tables.Table):
    user = tables.Column(verbose_name='유저명')
    gender = tables.Column(verbose_name='성별')
    series_of_class = tables.Column(verbose_name='직렬')
    second_exam_score = tables.Column(verbose_name='2차표준점수')
    nhi_score = tables.Column(verbose_name='연수원표준점수')
    total_score = tables.Column(verbose_name='단순합산점수')
    ranking = tables.Column(verbose_name='단순합산순위')
    prefer_1st = tables.Column(verbose_name='1지망')
    prefer_2nd = tables.Column(verbose_name='2지망')
    prefer_3rd = tables.Column(verbose_name='3지망')
    allocated_ministry = tables.Column(verbose_name='예상부처')

    class Meta:
        #model = UserProfile
        template_name = 'django_tables2/bootstrap-responsive.html'

# Table that
class ResultByMinistryTable(tables.Table):
    name = tables.Column(verbose_name='이름')
    gender = tables.Column()
    total_rank = tables.Column()
    preference = tables.Column()
    ministry_score = tables.Column()
    rank_by_ministry = tables.Column()

class AppliedDictionaryTable(tables.Table):
    applied_samugwan = tables.Column()

    def render_applied_samugwan(self, value):
        return value

class ApplyingSimulationTable(tables.Table):
    ministry_name_korean = tables.Column(verbose_name='부처명', attrs={'td':{'width': '25%'}})
    ministry_quota = tables.Column(verbose_name='TO')
    allocated_samugwan = tables.Column(verbose_name='예상배정자(등수)')

    def render_allocated_samugwan(self, value):
        string = ''
        if value:
            for item in value:
                string += '  {0},  '.format(item)
            return string
        else:
            return string

    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'
