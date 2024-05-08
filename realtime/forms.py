from django import forms

from realtime.models import TestModel


class TestForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = '__all__'
