from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from sogo_app.models import Results, Activities, UserProfile, GritActivity, GritChallenge
from datetime import date, datetime, timedelta
from django.forms.widgets import TextInput
#from django.utils.dateparse import parse_duration
from django.utils.dateparse import parse_duration
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django.forms.formsets import BaseFormSet
import pytz
from django.core.exceptions import ObjectDoesNotExist


class UserProfileForm(ModelForm):
    class Meta:
        fields = ("leaderboard", )
        model = UserProfile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leaderboard'].help_text= "* Select to show on leaderboard, unselect to hide results from leaderboard"


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2',)
        model = get_user_model()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label= "Display Name"
        self.fields['email'].label = "Email Address"
        self.fields['email'].help_text = '* Only used if you need to reset your password'
        self.fields['username'].help_text = '* You can use your real name or a nickname'
        self.fields['password1'].help_text = "* Password must be 8 characters"
        self.fields['password2'].help_text = "* Enter the same password as before, for verification."


class DateInput(forms.DateInput):
    input_type = 'date'


class LogResultsForm(ModelForm):
    class Meta:
        model = Results

        exclude = ['user']
        widgets = {
            'date': DateInput(),
            #'result': DurationInput()
        }

    def __init__(self, *args, **kwargs):
         self.request = kwargs.pop('request', None)
         self.mode = kwargs.pop('mode', None)

         super(LogResultsForm, self).__init__(*args, **kwargs)
         self.fields['notes'].label='Notes (Optional)'
         self.fields['activity'].label = "Activity - please select from the list to enter results"
         self.fields['date'].initial = date.today()
         self.fields['duration'].widget.attrs['placeholder'] = "MM:SS"
         self.fields['duration'].label="Time. Please enter MM:SS, for example 05:05 for 5 mins, 5 sec"
         self.fields['activity'].widget.attrs['id']="activity"
         self.fields['duration'].widget.attrs['id']="duration_field"
         self.fields['duration'].required = False
         self.fields['sets'].required = False
         self.fields['reps'].required = False

    def clean_duration(self):
        form_data = self.cleaned_data
        activity = Activities.objects.get(name=form_data['activity'])

        if activity.target_type == "T":
            try:
                entered_time = self.request.POST['duration']
                if entered_time[2] == ":":
                    if int(entered_time[0:2]) < 60:
                        if len(entered_time[3:5]) == 2 and int(entered_time[3:]) < 60:
                            pass
                        else:
                            self.errors['duration']=['SS must be 2 characters and less than 60']
                    else:
                        self.errors['duration']=['MM must be 2 characters and less than 60']
                else:
                    self.errors['duration']=['1 Invalid time, please enter a : between MM:SS']

            except TypeError:
                self.errors['duration']=['Invalid time, please enter MM:SS']
            except Exception as e:
                print ('error', e)
                self.errors['duration']=['Invalid time, please enter MM:SS']
        return form_data['duration']


    def clean(self, *args, **kwargs):
        form_data = super(LogResultsForm, self).clean()
        print (self.request.user, form_data)
        try:
            if self.mode != 'update':
                Results.objects.get(user=self.request.user, date=form_data['date'], activity=form_data['activity'])
                raise forms.ValidationError('A result for that day/activity already exists, please update, click STS Monthly Challenge (above), then My Results')
        except ObjectDoesNotExist:
            pass

        activity = Activities.objects.get(name=form_data['activity'])

        if activity.target_type == "R":
            if form_data['sets'] == None or form_data['reps'] == None:
                raise forms.ValidationError("Please enter values in Sets and Reps (0 if no reps)")
            elif form_data['sets'] <= 0:
                self.errors['sets'] = ['Please enter a number of sets, must be 1 or more']
        print ('leaving cleand_dur', form_data)
        return form_data


class CreateActivityForm(ModelForm):
    class Meta:
        model = Activities
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Activity Name"


class CreateGritChallengeForm(ModelForm):
    class Meta:
        model = GritChallenge
        fields = ('start_date',)
        widgets = {
            'start_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].label = ''
        self.fields['start_date'].initial = datetime.now(pytz.timezone("Asia/Tokyo")).date()


class CreateGritActivityForm(ModelForm):
    class Meta:
        model = GritActivity
        fields = ('date', 'count')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['count'].label = ''
        self.fields['date'].widget.attrs['readonly']=True
        self.fields['date'].label = ''
        self.fields['date'].widget.attrs['size']= '10'
        self.fields['count'].widget.attrs['class'] = 'count'
        if (self.instance.date) > datetime.now().date():
            self.fields['count'].widget.attrs['readonly']=True


#29 forms as today is a separate form and target is 30 days
BurpeeFormSet = modelformset_factory(GritActivity, form=CreateGritActivityForm, max_num=29)
