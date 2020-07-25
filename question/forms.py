from django import forms

class QuestionForm(forms.Form):
    query = forms.CharField()
    