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
    cut_off_date = '2018-10-01'
    activities = Activities.objects.all()
    result_dict = {}

    for activity in Activities.objects.all():
            data_list = []
            for user in User.objects.all():
                if len(Results.objects.filter(user=user, activity=activity, date__gte=cut_off_date).order_by('date')[:2]) > 1:


                    if activity.target_type == "T":
                        recent_result = Results.objects.filter(user__pk=user.pk, activity=activity).latest('date')
                        best_time = 0
                        for result in Results.objects.filter(user__pk=user.pk, activity=activity, date__gte=cut_off_date, date__lt=recent_result.date):
                            if best_time == 0 or result.duration < best_time:
                                best_time = result.duration

                        percent_change = ((best_time - recent_result.duration) / best_time) * 100
                        data = user, percent_change, recent_result.duration, best_time
                        data_list.append(data)
                    elif activity.target_type == "R":
                        recent_result = Results.objects.filter(user__pk=user.pk, activity=activity).latest('date')
                        best_result = 0
                        recent_float = float(recent_result.sets + ((recent_result.reps/(recent_result.sets + 1) * 4)))
                        print ('recent', recent_float)
                        for result in Results.objects.filter(user__pk=user.pk, activity=activity, date__gte=cut_off_date, date__lt=recent_result.date):

                            print (result.date, result.sets, result.reps)
                            decimal = result.reps/((result.sets +1) *4)
                            print (decimal)
                            result_float = float(result.sets + decimal)
                            print (result_float)
                            if best_result == 0 or result_float > best_result:
                                best_result = result_float

                        percent_change = ((best_result - recent_float) / best_result) * 100
                        data = user, percent_change, recent_float, best_result
                        data_list.append(data)

            data_list.sort(key=lambda x: x[1], reverse=True)
            result_dict[activity] = data_list

    print (result_dict)


get_schedule()
