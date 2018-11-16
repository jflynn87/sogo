from django.contrib import admin
from sogo_app.models import Activities, Results, UserProfile, GritActivity, GritChallenge

# Register your models here.

class ResultsAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'activity', 'duration',]
    list_filter = ['activity', 'date']


admin.site.register(Activities)
admin.site.register(Results, ResultsAdmin)
admin.site.register(UserProfile)
admin.site.register(GritChallenge)
admin.site.register(GritActivity)
