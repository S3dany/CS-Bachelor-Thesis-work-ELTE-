from django import forms
from .models import Report
import pandas as pd
from django.utils.translation import ugettext as _
import pycountry
import numpy as np


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', "data"]

    def clean_data(self):
        countries = []
        for country in pycountry.countries:
            countries.append(country.alpha_2)

        data_passed = self.cleaned_data.get("data")

        if not data_passed.name.endswith('.csv'):
            raise forms.ValidationError(_("Please upload a .csv file. this is the only format allowed"))

        df = pd.read_csv(data_passed.file)

        if not (df.columns[0] == "from" and df.columns[1] == "to" and df.columns[2] == "amount"):
            raise forms.ValidationError(_("Please fix the columns titles to the form (from , to , amount)"
                                          " in the exact order"))

        if not df['from'].isin(countries).all():
            raise forms.ValidationError(_("Please fix from countries to match the alpha2 country code "
                                          "(US, GB, HU, ...) in capital letters."))

        if not df['to'].isin(countries).all():
            raise forms.ValidationError(_("Please fix to countries to match the alpha2 country code "
                                        "(US, GB, HU, ...) in capital letters"))

        if pd.isna(df['amount']).any() or not np.issubdtype(df['amount'].dtype, np.number):

            raise forms.ValidationError(_("Please fix amounts to be all numbers and make sure there are "
                                          "no empty cells"))

        return data_passed
