from django.db import models


class RingoProductingArea(models.Model):
    # 割合は以下より
    # http://www.ringodaigaku.com/study/statistics/production.html
    pref = models.CharField('都道府県名', max_length=10)
    ratio = models.PositiveSmallIntegerField('割合', default=0)
