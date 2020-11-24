from django import forms

class originalDTForm(forms.Form):
  name = forms.CharField(label = "데이터 타입 명", max_length = 30, required=True, label_suffix="")
  schemainfo = forms.CharField(label = "스키마 정보", max_length = 200, required=True, label_suffix="")
  schematype = forms.CharField(label = "자료형 정보", max_length = 200, required=True, label_suffix="")
