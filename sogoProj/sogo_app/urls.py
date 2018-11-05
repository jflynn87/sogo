from django.conf.urls import include, url
from sogo_app import views
from django.contrib.auth import views as auth_views


app_name = 'sogo_app'

urlpatterns = [
    url(r'^signup/$', views.SignUp.as_view(),name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='sogo_app/login.html'),name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(),name='logout'),
    url(r'^log_results/$', views.LogResultsView.as_view(),name='log_results'),
    url(r'^create_activity/$', views.CreateActivityView.as_view(),name='create_activity'),
    url(r'^leaderboard/$', views.LeaderboardView.as_view(),name='leaderboard'),
    url(r'^my_results/$', views.MyResultsView.as_view(),name='my_results'),

    ]
