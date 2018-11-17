import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","sogoProj.settings")

import django
django.setup()
from sogo_app.models import User, UserProfile, Activities, Results
from datetime import datetime, timedelta
import sqlite3
from django.db.models import Sum, Min, Max

def get_schedule():

    import urllib3.request
    import urllib
    import urllib3
    from bs4 import BeautifulSoup

    # connection  = sqlite3.connect("db.sqlite3")
    #
    # cursor = connection.cursor()
    #
    # dropTableStatement = "DROP TABLE golf_app_tournament"
    #
    # cursor.execute(dropTableStatement)
    #
    # connection.close()

    #for user in User.objects.all():
    cut_off_date = '2018-10-01'
    activities = Activities.objects.all()
    for user in User.objects.all():
        for activity in activities:
            if len(Results.objects.filter(user=user, activity=activity, date__gte=cut_off_date).order_by('date')[:2]) > 1:
                ## need to get best prior result, getting current result
                recent_result = Results.objects.filter(user=user, activity=activity).latest('date')
                best_time = Results.objects.filter(user=user, activity=activity, date__gte=cut_off_date, date__lt=recent_result.date).aggregate(Min('duration'))

                percent_change = (best_time.get('duration__min') - recent_result.duration) / best_time.get('duration__min')
                print (user, recent_result.duration, best_time.get('duration__min'), percent_change)


get_schedule()
