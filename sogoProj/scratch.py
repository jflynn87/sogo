import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","sogoProj.settings")

import django
django.setup()
from sogo_app.models import User, UserProfile, Activities, Results, GritChallenge, GritActivity
from datetime import datetime, timedelta
import sqlite3
from django.db.models import Sum, Min, Max, Count

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
    #for challenge in GritChallenge.objects.all():
    print (GritActivity.objects.filter(count__gt=0).values('challenge__user__username').annotate(count=Sum('count'), days=Count('date')))

        #for activity in GritActivity.objects.filter(challenge=challenge):
        #    print (activity.challenge.user, activity.date, activity.count)



get_schedule()
