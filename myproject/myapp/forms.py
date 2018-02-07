from django import forms
from django.db.models.aggregates import Count
from localflavor.jp.jp_prefectures import JP_PREFECTURES
from localflavor.jp.forms import JPPrefectureCodeSelect, JPPrefectureSelect, JPPostalCodeField
from .models import RingoProductingArea


class MyForm(forms.Form):
    my_pref_code_ng = forms.ChoiceField(widget=JPPrefectureCodeSelect)
    my_pref_code_ok = forms.CharField(widget=JPPrefectureCodeSelect)
    my_pref_code_default = forms.CharField(widget=JPPrefectureCodeSelect, initial='20')
    my_pref_ng = forms.ChoiceField(widget=JPPrefectureSelect)
    my_pref_ok = forms.CharField(widget=JPPrefectureSelect)
    my_pref_default = forms.CharField(widget=JPPrefectureSelect, initial='nagano')
    my_postal_code = JPPostalCodeField()
    my_pref = forms.ChoiceField(label='全都道府県(choicesにセット)', choices=JP_PREFECTURES, initial='tokyo')
    limit_pref = forms.ChoiceField(label='Modelに存在する都道府県', choices=[('', '')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 都道府県が登録されているデータを取得する
        q = RingoProductingArea.objects.values_list('pref', flat=True)\
            .annotate(count_status=Count('pref'))\
            .filter(count_status__gt=0).distinct()
        # choicesの形(tupleのlist)にしておく
        product_prefs = [(pref, pref) for pref in q]

        # product_prefsと比較しやすいよう、JP_PREFECTURESを日本語表記の都道府県tupleのlistにしておく
        # 元々は、(ローマ字表記, 日本語表記)のtuple
        all_prefs_by_jp = [(pref_by_jp, pref_by_jp) for pref_by_en, pref_by_jp in JP_PREFECTURES]

        # 都道府県が登録されているデータだけにする
        exists_prefs = [pref for pref in all_prefs_by_jp if pref in product_prefs]
        # 先頭にメッセージを入れる
        exists_prefs.insert(0, ('', '都道府県を選ぶ'))
        # limit_prefフィールドのchoicesとして設定
        self.fields['limit_pref'].choices = exists_prefs
        # とはえ、初期値は別のもの
        self.fields['limit_pref'].initial = '長野県'
