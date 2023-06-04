from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Customer
