from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from sogo_app.models import Results, Activities

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label= "Display Name"
        self.fields['email'].label = "Email Address"
        self.fields['username'].help_text = '* You can use your real name or a nickname'

class LogResultsForm(ModelForm):
    class Meta:
        model = Results
        exclude = ['user']
        widgets = {
            'date': forms.DateInput(attrs={'class':'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['notes'].help_text='Notes Are Optional'


class CreateActivityForm(ModelForm):
    class Meta:
        model = Activities
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Activity Name"
