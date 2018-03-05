# Generated by Django 2.0.2 on 2018-03-05 07:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ministry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ministry_name', models.CharField(choices=[('BAI', '감사원'), ('MOEL', '고용노동부'), ('KFTC', '공정거래위원회'), ('MSIT', '과학기술정보통신부'), ('KCS', '관세청'), ('MOE', '교육부'), ('MPVA', '국가보훈처'), ('NHRC', '국가인권위원회'), ('OPC', '국무총리실'), ('ACRC', '국민권익위원회'), ('MND', '국방부'), ('NTS', '국세청'), ('MOLIT', '국토교통부'), ('FSC', '금융위원회'), ('MOSF', '기획재정부'), ('MAFRA', '농림축산식품부'), ('CHA', '문화재청'), ('MCST', '문화체육관광부'), ('KCC', '방송통신위원회'), ('DAPA', '방위사업청'), ('MOLEG', '법제처'), ('MMA', '병무청'), ('MOHW', '보건복지부'), ('KFS', '산림청'), ('MOTIE', '산업통상자원부'), ('SDIA', '새만금개발청'), ('MFDS', '식품의약품안전처'), ('MOGEF', '여성가족부'), ('MPM', '인사혁신처'), ('PPS', '조달청'), ('MSS', '중소벤처기업부'), ('NEC', '중앙선거관리위원회'), ('KOSTAT', '통계청'), ('MOU', '통일부'), ('KIPO', '특허청'), ('MOF', '해양수산부'), ('MOIS', '행정안전부'), ('NAACC', '행정중심복합도시건설청'), ('ME', '환경부')], max_length=20)),
                ('ministry_quota', models.IntegerField(default=0)),
                ('series_of_class', models.CharField(choices=[('general_admin', '일반행정'), ('econ_admin', '재경'), ('others_admin', '기타직렬')], max_length=20)),
                ('applied_samugwan', jsonfield.fields.JSONField(default=dict)),
                ('number_of_applicants', models.IntegerField(default=0)),
                ('second_exam_ratio', models.FloatField(default=0)),
                ('NHI_score_ratio', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('female', '여성'), ('male', '남성')], default='female', max_length=6)),
                ('passed_year', models.CharField(choices=[('year_before', '2014년 이전'), ('year_2015', '2015년'), ('year_2016', '2016년')], default='year_2016', max_length=20)),
                ('series_of_class', models.CharField(choices=[('general_admin', '일반행정'), ('econ_admin', '재경'), ('others_admin', '기타직렬')], default='general_admin', max_length=20)),
                ('second_exam_score', models.FloatField(default=0)),
                ('nhi_score', models.FloatField(default=0)),
                ('other_score_1st', models.FloatField(default=0)),
                ('other_score_2nd', models.FloatField(default=0)),
                ('other_score_3rd', models.FloatField(default=0)),
                ('total_score', models.FloatField(default=0)),
                ('ranking', models.IntegerField(default=0)),
                ('prefer_1st', models.CharField(choices=[('BAI', '감사원'), ('MOEL', '고용노동부'), ('KFTC', '공정거래위원회'), ('MSIT', '과학기술정보통신부'), ('KCS', '관세청'), ('MOE', '교육부'), ('MPVA', '국가보훈처'), ('NHRC', '국가인권위원회'), ('OPC', '국무총리실'), ('ACRC', '국민권익위원회'), ('MND', '국방부'), ('NTS', '국세청'), ('MOLIT', '국토교통부'), ('FSC', '금융위원회'), ('MOSF', '기획재정부'), ('MAFRA', '농림축산식품부'), ('CHA', '문화재청'), ('MCST', '문화체육관광부'), ('KCC', '방송통신위원회'), ('DAPA', '방위사업청'), ('MOLEG', '법제처'), ('MMA', '병무청'), ('MOHW', '보건복지부'), ('KFS', '산림청'), ('MOTIE', '산업통상자원부'), ('SDIA', '새만금개발청'), ('MFDS', '식품의약품안전처'), ('MOGEF', '여성가족부'), ('MPM', '인사혁신처'), ('PPS', '조달청'), ('MSS', '중소벤처기업부'), ('NEC', '중앙선거관리위원회'), ('KOSTAT', '통계청'), ('MOU', '통일부'), ('KIPO', '특허청'), ('MOF', '해양수산부'), ('MOIS', '행정안전부'), ('NAACC', '행정중심복합도시건설청'), ('ME', '환경부')], default='', max_length=20)),
                ('prefer_2nd', models.CharField(choices=[('BAI', '감사원'), ('MOEL', '고용노동부'), ('KFTC', '공정거래위원회'), ('MSIT', '과학기술정보통신부'), ('KCS', '관세청'), ('MOE', '교육부'), ('MPVA', '국가보훈처'), ('NHRC', '국가인권위원회'), ('OPC', '국무총리실'), ('ACRC', '국민권익위원회'), ('MND', '국방부'), ('NTS', '국세청'), ('MOLIT', '국토교통부'), ('FSC', '금융위원회'), ('MOSF', '기획재정부'), ('MAFRA', '농림축산식품부'), ('CHA', '문화재청'), ('MCST', '문화체육관광부'), ('KCC', '방송통신위원회'), ('DAPA', '방위사업청'), ('MOLEG', '법제처'), ('MMA', '병무청'), ('MOHW', '보건복지부'), ('KFS', '산림청'), ('MOTIE', '산업통상자원부'), ('SDIA', '새만금개발청'), ('MFDS', '식품의약품안전처'), ('MOGEF', '여성가족부'), ('MPM', '인사혁신처'), ('PPS', '조달청'), ('MSS', '중소벤처기업부'), ('NEC', '중앙선거관리위원회'), ('KOSTAT', '통계청'), ('MOU', '통일부'), ('KIPO', '특허청'), ('MOF', '해양수산부'), ('MOIS', '행정안전부'), ('NAACC', '행정중심복합도시건설청'), ('ME', '환경부')], default='', max_length=20)),
                ('prefer_3rd', models.CharField(choices=[('BAI', '감사원'), ('MOEL', '고용노동부'), ('KFTC', '공정거래위원회'), ('MSIT', '과학기술정보통신부'), ('KCS', '관세청'), ('MOE', '교육부'), ('MPVA', '국가보훈처'), ('NHRC', '국가인권위원회'), ('OPC', '국무총리실'), ('ACRC', '국민권익위원회'), ('MND', '국방부'), ('NTS', '국세청'), ('MOLIT', '국토교통부'), ('FSC', '금융위원회'), ('MOSF', '기획재정부'), ('MAFRA', '농림축산식품부'), ('CHA', '문화재청'), ('MCST', '문화체육관광부'), ('KCC', '방송통신위원회'), ('DAPA', '방위사업청'), ('MOLEG', '법제처'), ('MMA', '병무청'), ('MOHW', '보건복지부'), ('KFS', '산림청'), ('MOTIE', '산업통상자원부'), ('SDIA', '새만금개발청'), ('MFDS', '식품의약품안전처'), ('MOGEF', '여성가족부'), ('MPM', '인사혁신처'), ('PPS', '조달청'), ('MSS', '중소벤처기업부'), ('NEC', '중앙선거관리위원회'), ('KOSTAT', '통계청'), ('MOU', '통일부'), ('KIPO', '특허청'), ('MOF', '해양수산부'), ('MOIS', '행정안전부'), ('NAACC', '행정중심복합도시건설청'), ('ME', '환경부')], default='', max_length=20)),
                ('allocated_ministry', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
