from django.conf.urls import include, url
from sogo_app import views
from django.contrib.auth import views as auth_views


app_name = 'sogo_app'

urlpatterns = [
    url(r'^signup/$', views.SignUp.as_view(),name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='sogo_app/login.html'),name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(),name='logout'),
    url(r'^log_results/$', views.LogResultsView.as_view(),name='log_results'),
    url(r'^update_results/(?P<pk>\d+)/$', views.ResultsUpdateView.as_view(),name='update_results'),
    url(r'^delete_results/(?P<pk>\d+)/$', views.ResultsDeleteView.as_view(),name='delete_results'),
    url(r'^create_activity/$', views.CreateActivityView.as_view(),name='create_activity'),
    url(r'^update_activity/(?P<pk>\d+)/$', views.UpdateActivityView.as_view(),name='update_activity'),
    url(r'^delete_activity/(?P<pk>\d+)/$', views.DeleteActivityView.as_view(),name='delete_activity'),
    url(r'^activity_list/$', views.ActivityListView.as_view(),name='activity_list'),
    url(r'^leaderboard/$', views.LeaderboardView.as_view(),name='leaderboard'),
    url(r'^my_results/$', views.MyResultsView.as_view(),name='my_results'),
    url(r'^create_grit/$', views.CreateGritChallengeView.as_view(),name='create_grit'),
    url(r'^delete_grit/(?P<pk>\d+)/$', views.DeleteGritChallengeView.as_view(),name='delete_grit'),
    url(r'^grit_list/$', views.CreateGritActivityView.as_view(),name='grit_list'),
    url(r'^ajax/get_target_type/$', views.get_target_type, name='get_target_type'),

    ]
