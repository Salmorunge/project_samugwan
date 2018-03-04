from decimal import Decimal

ministry_name_choices = (
    ('BAI', '감사원'), ('MOEL', '고용노동부'), ('KFTC', '공정거래위원회'), ('MSIT', '과학기술정보통신부'),
    ('KCS', '관세청'), ('MOE', '교육부'), ('MPVA', '국가보훈처'), ('NHRC', '국가인권위원회'), ('OPC', '국무총리실'), ('ACRC', '국민권익위원회'),
    ('MND', '국방부'), ('NTS', '국세청'), ('MOLIT', '국토교통부'), ('FSC', '금융위원회'), ('MOSF', '기획재정부'),
    ('MAFRA', '농림축산식품부'), ('CHA', '문화재청'), ('MCST', '문화체육관광부'), ('KCC', '방송통신위원회'),
    ('DAPA', '방위사업청'), ('MOLEG', '법제처'), ('MMA', '병무청'), ('MOHW', '보건복지부'), ('KFS', '산림청'),
    ('MOTIE', '산업통상자원부'), ('SDIA', '새만금개발청'), ('MFDS', '식품의약품안전처'), ('MOGEF', '여성가족부'),
    ('MPM', '인사혁신처'), ('PPS', '조달청'), ('MSS', '중소벤처기업부'), ('NEC', '중앙선거관리위원회'), ('KOSTAT', '통계청'),
    ('MOU', '통일부'), ('KIPO', '특허청'), ('MOF', '해양수산부'), ('MOIS', '행정안전부'), ('NAACC', '행정중심복합도시건설청'),
    ('ME', '환경부')
)


def calculate_ministry_score(userprofile, ministry, other_score):

    ministry_score = Decimal(userprofile.second_exam_score * ministry.second_exam_ratio + userprofile.nhi_score * ministry.NHI_score_ratio + other_score)
    ministry_score = round(ministry_score,2)
    ministry_score = float(ministry_score)

    return ministry_score
