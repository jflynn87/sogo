from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta

from sogo_app import forms
from sogo_app.models import Results, Activities

from pytimeparse.timeparse import timeparse

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
    #template_name = 'sogo_app/create_activity.html'

class LogResultsView(LoginRequiredMixin, CreateView):
    login_url = '/sogo_app/login'
    form_class=forms.LogResultsForm
    model=Results
    success_url = reverse_lazy('sogo_app:my_results')


    # def dispatch(self, request, *args, **kwargs):
    #     if request.POST:
    #         print ('dispatch')
    #         result= request.POST['result']
    #         duration = timeparse(result)
    #         print (duration)
    #         kwargs['result_duration'] = duration


    #    return super(LogResultsView, self).dispatch(request, *args, **kwargs)



    def form_valid(self, form):

        result = form.save(commit=False)
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
        activity_dict = {}


        cut_off_date = datetime.today() - timedelta(days=90)
        print (cut_off_date)
        for activity in Activities.objects.filter(track=True):
            print (activity)
            result_dict = {}
            for user in User.objects.all():
                #print ('user', user)
                result_list=[]
                if len(Results.objects.filter(activity=activity, user__pk=user.pk, date__gte=cut_off_date).order_by('date')[:2]) > 1:
                    #print ('in results')
                    result_list.append(user.username)
                    for result in Results.objects.filter(activity=activity, user__pk=user.pk).order_by('date')[:2]:
                        result_list.append(str(result.date))
                        result_list.append(result.result)
                    percentage_change = ((result_list[2]-result_list[4])/result_list[2])*100
                    result_list.append(percentage_change)

                    try:

                        activity_dict[activity].append(result_list)
                    except KeyError:
                        print(result_list)
                        activity_dict[activity] = result_list
                    except Exception as e:
                        print ('execption', e)

        print ('act dict', activity_dict)
        # sort the results by the % change which is the last item in the result_list
        display_dict = {}
        sorted_results_list = []
        #for key, value in activity_dict.items():

        for activity, result in sorted(activity_dict.items(), key=lambda x:x[1][5], reverse=True):
            display_dict[activity]=result


        context.update({
          'result_dict': display_dict,
         })
        return context

class ResultsUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/sogo_app/login'
    form_class = forms.LogResultsForm
    success_url=reverse_lazy('sogo_app:my_results')
    model = Results

class ResultsDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/sogo_app/login'
    model = Results
    success_url = reverse_lazy('sogo_app:my_results')


class MyResultsView(LoginRequiredMixin, ListView):
    login_url= '/sogo_app/login'
    model=Results

    def get_context_data(self,**kwargs):
        context = super(MyResultsView, self).get_context_data(**kwargs)
        context.update({
        'object_list': Results.objects.filter(user=self.request.user),
        })
        return context

class MyResultsDetailView(LoginRequiredMixin, DetailView):
    login_url= '/sogo_app/login'
    model = Results
    template_name = 'sogo_app/result_detail.html'
