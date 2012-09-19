#-*- coding: UTF-8 -*-
from datetime import date, timedelta
from django import forms


class DateRangeForm(forms.Form):
    """
    Form that represents a date range

    This form is always bound
    """
    start_date = forms.DateField(initial=date.today() - timedelta(days=30),
        label='Fecha de inicio')
    end_date = forms.DateField(initial=date.today(),
        label=u'Fecha de término')

    def __init__(self, data=None, *args, **kwargs):
        if not data:
            data = dict()

        if 'start_date' not in data and 'end_date' not in data:
            data = data.copy()
            data['start_date'], data['end_date'] =\
            DateRangeForm.default_dates()

        super(DateRangeForm, self).__init__(data, *args, **kwargs)

    def clean_end_date(self):
        d = self.cleaned_data

        if 'start_date' in d and 'end_date' in d:
            if d['end_date'] < d['start_date']:
                raise forms.ValidationError(u'La fecha de término debe ser '
                                            u'posterior a la fecha de inicio')

        return d['end_date']

    @classmethod
    def default_dates(cls):
        f = getattr(cls, 'base_fields')
        return f['start_date'].initial, f['end_date'].initial
