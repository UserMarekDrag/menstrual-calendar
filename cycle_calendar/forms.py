from django.forms import ModelForm, DateInput
from .models import UserCalendar, UserCalendarDate, UniqueTextShare, UserShareCalendar
from django import forms


class UserCalendarDateForm(ModelForm):
    class Meta:
        model = UserCalendarDate

        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        fields = ('start_time',
                  )

    def __init__(self, *args, **kwargs):
        super(UserCalendarDateForm, self).__init__(*args, **kwargs)

        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%d',)


class UserCalendarForm(forms.ModelForm):
    class Meta:
        model = UserCalendar
        fields = ('cycle_length',
                  'first_phase_length',
                  )


class UniqueTextShareForm(forms.ModelForm):
    class Meta:
        model = UniqueTextShare
        fields = ('unique_text',
                  )


class UserShareCalendarForm(forms.ModelForm):
    class Meta:
        model = UserShareCalendar
        fields = '__all__'
