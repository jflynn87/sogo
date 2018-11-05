from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

from sogo_app import forms
from sogo_app. models import Results

# Create your views here.

class HomePage(TemplateView):
    template_name='index.html'

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('sogo_app:login')
    template_name = 'sogo_app/signup.html'

class CreateActivityView(LoginRequiredMixin, CreateView):
    login_url = '/sogo_app/login'
    form_class=forms.CreateActivityForm
    success_url=reverse_lazy('index')
    template_name = 'sogo_app/create_activity.html'


class LogResultsView(LoginRequiredMixin, CreateView):
    login_url = '/sogo_app/login'
    form_class=forms.LogResultsForm
    success_url = reverse_lazy('index')  #update this to leaderboard or somewhere else
    template_name = 'sogo_app/log_results.html'

    def form_valid(self, form):
        result = form.save(commit=False)
        #print (result)
        #print (self.request.user.pk)
        print ('users', User.objects.all())

        result.user = User.objects.get(pk=self.request.user.pk)
        result.save()
        return HttpResponseRedirect(self.success_url)

class LeaderboardView(LoginRequiredMixin, ListView):
    login_url= '/sogo_app/login'
    model=Results
    template_name = 'sogo_app/leaderboard.html'

    def get_context_data(self,**kwargs):
        context = super(LeaderboardView, self).get_context_data(**kwargs)
        result_dict = {}

        for user in User.objects.all():
            result_list=[]
            if len(Results.objects.filter(activity__track=True, user__pk=user.pk).order_by('date')[:2]) > 1:
                for result in Results.objects.filter(activity__track=True, user__pk=user.pk).order_by('date')[:2]:
                    result_list.append(str(result.date))
                    result_list.append(result.result)
                percentage_change = ((result_list[1]-result_list[3])/result_list[1])*100
                result_list.append(percentage_change)
                result_dict[user]=result_list
        print (result_dict)

        context.update({
          'result_dict': result_dict,
         })
        return context


class MyResultsView(LoginRequiredMixin, ListView):
    login_url= '/sogo_app/login'
    model=Results

    def get_context_data(self,**kwargs):
        context = super(MyResultsView, self).get_context_data(**kwargs)
        context.update({
        'object_list': Results.objects.filter(user=self.request.user),
        })
        return context
