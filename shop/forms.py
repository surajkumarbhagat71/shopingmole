from django import forms
from shop.models import *


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user',)