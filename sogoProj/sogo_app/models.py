from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class User(auth.models.User,auth.models.PermissionsMixin):

#    def __str__(self):
#        return "@{}".format(self.username)


class Activities(models.Model):
    TARGET_TYPES = (('T', 'Time'),
                    ('R', 'Reps'))
    name = models.CharField(max_length=100, unique=True)
    beginner_target = models.CharField(max_length=100)
    expert_target = models.CharField(max_length=100)
    target_type = models.CharField(max_length=1, choices=TARGET_TYPES)
    track = models.BooleanField()

    def __str__(self):
        return self.name


class Results(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE)
    result = models.DurationField()
    notes = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        unique_together = ('date', 'activity', 'user')

    def __str__(self):
        return str(self.date) + ' - ' +str(self.activity)
