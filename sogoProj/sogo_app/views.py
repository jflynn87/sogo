from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta, tzinfo
import pytz

from sogo_app import forms
from sogo_app.models import Results, Activities, GritActivity, GritChallenge

from django.core.exceptions import ObjectDoesNotExist
from collections import defaultdict
from django.db.models import Sum



#from pytimeparse.timeparse import timeparse

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
    model = Activities
    success_url=reverse_lazy('index')

class UpdateActivityView(LoginRequiredMixin, UpdateView):
    login_url = '/sogo_app/login'
    form_class = forms.CreateActivityForm
    success_url=reverse_lazy('sogo_app:activity_list')
    model = Activities

class DeleteActivityView(LoginRequiredMixin, DeleteView):
    login_url = '/sogo_app/login'
    model = Activities
    success_url = reverse_lazy('sogo_app:activity_list')


class ActivityListView(LoginRequiredMixin, ListView):
    login_url = '/sogo_app/login'
    model = Activities


class LogResultsView(LoginRequiredMixin, CreateView):
    login_url = '/sogo_app/login'
    form_class=forms.LogResultsForm
    model=Results
    success_url = reverse_lazy('sogo_app:my_results')


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
            for user in User.objects.all():
                result_list=[]
                if len(Results.objects.filter(activity=activity, user__pk=user.pk, date__gte=cut_off_date).order_by('date')[:2]) > 1:
                    result_list.append(user.username)
                    for result in Results.objects.filter(activity=activity, user__pk=user.pk).order_by('date')[:2]:
                        result_list.append(str(result.date))
                        result_list.append(result.duration)
                    percentage_change = ((result_list[2]-result_list[4])/result_list[2])*100
                    result_list.append(percentage_change)

                    activity_dict.setdefault(activity, []).append(result_list)

                    # if activity_dict.get(activity):
                    #     result = activity_dict.get(activity)
                    #     activity_dict[activity] = result, result_list
                    #     print (activity_dict)
                    # else:
                    #     #print(result_list)
                    #     activity_dict[activity]= result_list
                    #     print (activity_dict)

        #print ('act dict', activity_dict)
        # sort the results by the % change which is the last item in the result_list
        display_dict = {}
        sorted_results_list = []
        #for key, value in activity_dict.items():
        #    print (value)
        #print (activity_dict)
        print (activity_dict)
        for k, v in sorted(activity_dict.items(), key=lambda v: v[1][0][5], reverse=True):

#        for activity, result in sorted(activity_dict.items(), key=lambda x:x[1][5], reverse=True):
#                print (activity, result)
              display_dict[k]=v


        context.update({
          #'result_dict': display_dict,
          'result_dict': display_dict
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

class CreateGritChallengeView(LoginRequiredMixin, CreateView):
    login_url= '/sogo_app/login'
    model = GritChallenge
    success_url = reverse_lazy('sogo_app:grit_list')
    form_class = forms.CreateGritChallengeForm

    def get_context_data(self,**kwargs):
        context = super(CreateGritChallengeView, self).get_context_data(**kwargs)

        try:
            form = forms.CreateGritChallengeForm(instance=GritChallenge.objects.get(user=self.request.user))
        except ObjectDoesNotExist:
            form = forms.CreateGritChallengeForm()
        context.update({
                'form': form,
                })
        return context

    def form_valid(self, form):
        plan = form.save(commit=False)
        plan.user = User.objects.get(pk=self.request.user.pk)
        plan.target_date = plan.start_date + timedelta(days=29)
        plan.save()

        return HttpResponseRedirect(self.success_url)

class CreateGritActivityView(LoginRequiredMixin, ListView):
    login_url= '/sogo_app/login'
    model = GritActivity
    success_url = reverse_lazy('sogo_app:grit_list')
    form_class = forms.CreateGritActivityForm

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('sogo_app:login'))
        if not GritActivity.objects.filter(challenge__user=self.request.user).exists():
            return HttpResponseRedirect(reverse('sogo_app:create_grit'))
        else:
            return super(CreateGritActivityView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        context = super(CreateGritActivityView, self).get_context_data(**kwargs)
        print (self.request )
        data = self.build_data()
        message = "Please enter the number of burpees per day. You can only enter for today or past dates."

        context.update({
            'today': data[0],
            'form': data[1],
            'summary_list': data[2],
            'message': message
        })
        return context

    def post(self, request):

        print (request.user)
        try:
            GritActivity.objects.filter(challenge__user=request.user,date=request.POST['date']).update(count=request.POST['count'])
        except Exception as e:
            print ("today save issue", request.user, e)

        formset = forms.BurpeeFormSet(request.POST)

        if formset.is_valid():
            for form in formset:
                cd = form.cleaned_data
                GritActivity.objects.filter(challenge__user=request.user,date=cd['date']).update(count=cd['count'])

        data = self.build_data()
        message = "Updates Successful"

        return render(request, 'sogo_app/gritactivity_list.html', {
                        'today': data[0],
                        'form': data[1],
                        'summary_list': data[2],
                        'message': "Updates Successful."})

    def build_data(self):
        tz = pytz.timezone("Asia/Tokyo")

        form_today = forms.CreateGritActivityForm(instance=GritActivity.objects.get(challenge__user=self.request.user, date=datetime.now(tz)))

        form = forms.BurpeeFormSet(queryset=GritActivity.objects.filter(challenge__user=self.request.user).exclude(date=datetime.now(tz).date()))

        summary_list = []
        original_target = 1000
        completed = GritActivity.objects.filter(challenge__user=self.request.user).aggregate(Sum('count'))
        penalty = len(GritActivity.objects.filter(challenge__user=self.request.user, date__lt=datetime.now(pytz.timezone("Asia/Tokyo")).date(), count=0)) * 100
        remaining = (original_target + penalty) - completed.get('count__sum')
        target = original_target + penalty
        complete_percent = completed.get('count__sum')/target * 100
        percent_complete_format = ("{0:.2f}%".format(complete_percent))
        summary_list = [remaining, completed.get('count__sum'), target, percent_complete_format, penalty]

        return form_today, form, summary_list
