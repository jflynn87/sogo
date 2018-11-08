from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from sogo_app.models import Results, Activities
from datetime import date, datetime, timedelta
from django.forms.widgets import TextInput
from django.utils.dateparse import parse_duration

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label= "Display Name"
        self.fields['email'].label = "Email Address"
        self.fields['username'].help_text = '* You can use your real name or a nickname'

class DateInput(forms.DateInput):
    input_type = 'date'


class LogResultsForm(ModelForm):
    class Meta:
        model = Results
        exclude = ['user']
        widgets = {
            'date': DateInput(),
            'result': forms.TextInput()
        }

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['notes'].label='Notes (Optional)'
         self.fields['date'].initial = date.today()
         #self.fields['result'].widget.attrs['placeholder'] = "MM:SS"
         self.fields['result'].widget.attrs['class'] = "timing"



    def clean(self):
           form_data = self.cleaned_data
           try:
                  print (self.cleaned_data)
                  form_data = self.cleaned_data
                  time = (form_data['result'])
                  print ('time', time)
                  datetime.strptime(str(time), "%H:%M:%S")
                  if time  < timedelta(minutes=5):
                     self.errors['result'] = ["time too short, please re-confirm"]

           except ValueError:
                  print ('val error')
                  self.errors['result'] = ["format must be MM:SS"]
           except Exception as e:
                  print("other errir", e)
                  self.errors['result'] = ["format must be MM:SS"]
           print ('returning')
           print (form_data)
           return form_data

# class UpdateResultsForm(ModelForm):
#     class Meta:
#         model = Results
#         exclude = ['user']
#         widgets = {
#             'date': DateInput(),
#         }
#
#     def __init__(self, *args, **kwargs):
#          super().__init__(*args, **kwargs)
#          self.fields['notes'].label='Notes (Optional)'
#          self.fields['date'].initial = date.today()
#          #self.fields['result'].widget.attrs['placeholder'] = "MM:SS"
#
#
#     def clean(self):
#            form_data = self.cleaned_data
#            try:
#                   print (self.cleaned_data)
#                   form_data = self.cleaned_data
#                   time = (form_data['result'])
#                   print ('time', time)
#                   datetime.strptime(str(time), "%H:%M:%S")
#                   if time  < timedelta(minutes=5):
#                      self.errors['result'] = ["time too short, please re-confirm"]
#
#            except ValueError:
#                   print ('val error')
#                   self.errors['result'] = ["format must be MM:SS"]
#            except Exception as e:
#                   print("other errir", e)
#                   self.errors['result'] = ["format must be MM:SS"]
#            print ('returning')
#            print (form_data)
#            return form_data
#


class CreateActivityForm(ModelForm):
    class Meta:
        model = Activities
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Activity Name"
