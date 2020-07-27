from django import forms

class QuestionForm(forms.Form):
    query = forms.CharField(required=False)
    user= forms.CharField(required=False)
    tag = forms.CharField(required=False)
    