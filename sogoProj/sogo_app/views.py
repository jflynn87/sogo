from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
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
#imports for target_type json
from django.http import JsonResponse
import json



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

    def get_context_data(self, **kwargs):
        context = super(DeleteActivityView, self).get_context_data(**kwargs)
        results = Results.objects.filter(activity=self.object)

        context.update({
        'results': results
        })
        return context


class ActivityListView(LoginRequiredMixin, ListView):
    login_url = '/sogo_app/login'
    model = Activities


class LogResultsView(LoginRequiredMixin, CreateView):
    login_url = '/sogo_app/login'
    form_class=forms.LogResultsForm
    model=Results
    success_url = reverse_lazy('sogo_app:my_results')


    def get_form_kwargs(self):
        kw = super(LogResultsView, self).get_form_kwargs()
        kw['request'] = self.request # the trick!
        return kw


    def form_valid(self, form):

        result = form.save(commit=False)

        result.user = User.objects.get(pk=self.request.user.pk)
        result.save()
        return HttpResponseRedirect(self.success_url)

def get_target_type(request):
    if request.is_ajax():
        print (request.GET['activity'])
        activity = Activities.objects.get(pk=request.GET['activity'])
        data = json.dumps(activity.target_type)
        return HttpResponse(data, content_type="appliation/json")



class LeaderboardView(LoginRequiredMixin, ListView):
    login_url= '/sogo_app/login'
    model=Results
    template_name = 'sogo_app/leaderboard.html'

    def get_context_data(self,**kwargs):
        context = super(LeaderboardView, self).get_context_data(**kwargs)
        result_dict = {}

        cut_off_date = datetime.today() - timedelta(days=100)
        print (cut_off_date)

        for activity in Activities.objects.all():
            data_list = []
            for user in User.objects.all():
                if len(Results.objects.filter(user=user, activity=activity, date__gte=cut_off_date).order_by('date')[:2]) > 1:
                    recent_result = Results.objects.filter(user__pk=user.pk, activity=activity).latest('date')

                    if activity.target_type == "T":
                        best_time = 0
                        for result in Results.objects.filter(user__pk=user.pk, activity=activity, date__gte=cut_off_date, date__lt=recent_result.date):
                            if best_time == 0 or result.duration < best_time:
                                best_time = result.duration

                        percent_change = ((best_time - recent_result.duration) / best_time) * 100
                        data = user, round(percent_change), recent_result.duration, best_time
                        data_list.append(data)
                    elif activity.target_type == "R":
                        recent_result = Results.objects.filter(user__pk=user.pk, activity=activity).latest('date')
                        best_result = 0
                        recent_float = float(recent_result.sets + (recent_result.reps/((recent_result.sets + 1) * 4)))

                        for result in Results.objects.filter(user__pk=user.pk, activity=activity, date__gte=cut_off_date, date__lt=recent_result.date):
                            result_float = float(result.sets + (result.reps/((result.sets + 1) * 4)))
                            if best_result == 0 or result_float > best_result:
                                best_result = result_float

                        #percent_change = ((best_result - recent_float) / best_result) * 100
                        percent_change = ((recent_float - best_result) / recent_float) * 100
                        data = user, round(percent_change), "{0:.2f}".format(recent_float), "{0:.2f}".format(best_result)
                        data_list.append(data)


            if len(data_list) > 0:
                data_list.sort(key=lambda x: x[1], reverse=True)
                result_dict[activity] = data_list

        context.update({
          #'result_dict': display_dict,
          'result_dict': result_dict
         })
        return context

class ResultsUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/sogo_app/login'
    form_class = forms.LogResultsForm
    success_url=reverse_lazy('sogo_app:my_results')
    model = Results

    def get_form_kwargs(self):
        kw = super(ResultsUpdateView, self).get_form_kwargs()
        kw['request'] = self.request # the trick!
        kw['mode'] = 'update'
        return kw


class ResultsDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/sogo_app/login'
    model = Results
    success_url = reverse_lazy('sogo_app:my_results')

    def get_form_kwargs(self):
        kw = super(ResultsDeleteView, self).get_form_kwargs()
        kw['request'] = self.request # the trick!
        return kw


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


        context.update({
            'today': data[0],
            'form': data[1],
            'summary_list': data[2],
            'message': data[3]
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

        return render(request, 'sogo_app/gritactivity_list.html', {
                        'today': data[0],
                        'form': data[1],
                        'summary_list': data[2],
                        'message': data[3]})

    def build_data(self):
        tz = pytz.timezone("Asia/Tokyo")

        try:
            form_today = forms.CreateGritActivityForm(instance=GritActivity.objects.get(challenge__user=self.request.user, date=datetime.now(tz)))
        except Exception:
            form_today = ''


        form = forms.BurpeeFormSet(queryset=GritActivity.objects.filter(challenge__user=self.request.user).exclude(date=datetime.now(tz).date()))

        summary_list = []
        original_target = 1000
        completed = GritActivity.objects.filter(challenge__user=self.request.user).aggregate(Sum('count'))
        penalty = len(GritActivity.objects.filter(challenge__user=self.request.user, date__lt=datetime.now(pytz.timezone("Asia/Tokyo")).date(), count=0)) * 100
        remaining = (original_target + penalty) - completed.get('count__sum')
        target = original_target + penalty
        complete_percent = (completed.get('count__sum'))/target * 100
        percent_complete_format = ("{0:.2f}%".format(complete_percent))
        start_date = GritActivity.objects.filter(challenge__user=self.request.user).earliest('date')
        if self.request.POST:
            message = "Updates Successful"
        else:
            message = "Please enter the number of burpees per day. You can only enter for today or past dates."

        if GritActivity.objects.filter(challenge__user=self.request.user, count=0, date=datetime.now(tz).date()).exists():
            remaining_days = remaining_days =   timedelta(days=30) - (datetime.now(tz).date() - start_date.date)
        else:
            remaining_days =   timedelta(days=29) - (datetime.now(tz).date() - start_date.date)

        if remaining_days.days != 0:
            average = remaining/remaining_days.days
            average_format = average_format = ("{0:.1f}".format(average))
        elif remaining_days.days == 0 and  remaining <= 0:
            average_format = 0
            message = "Congratualtions, you have completed the GRIT Burpee Challenge!"
        else:
            average_format = remaining

        summary_list = [remaining, completed.get('count__sum'), average_format, target, percent_complete_format, penalty]

        return form_today, form, summary_list, message

class DeleteGritChallengeView(LoginRequiredMixin, DeleteView):
    login_url = '/sogo_app/login'
    model = GritChallenge
    success_url = reverse_lazy('sogo_app:create_grit')
