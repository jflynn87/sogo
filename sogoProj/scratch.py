import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","sogoProj.settings")

import django
django.setup()
from sogo_app.models import User, UserProfile
from datetime import datetime, timedelta
import sqlite3

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
    for user in User.objects.all():
        print (user)
    for user in UserProfile.objects.all():
        print (user, user.leaderboard)




get_schedule()
