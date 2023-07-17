from django.db import models
from django.contrib.auth.models import User
import datetime

STATE_CHOICES = ((0, 'در حال پیگیری'), (1, 'لغو شده'), (2, 'قرارداد بسته شده'))

class Project(models.Model):
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='employee'  
    )
    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='employer'
    )

    connection = models.CharField(max_length=256, null=True, blank=True)
    registered_date = models.DateField(auto_now_add=True)
    check_date = models.CharField(default='', max_length=512)
    how_meet = models.CharField(max_length=256, null=True, blank=True)
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=0)
    level = models.CharField(default='', max_length=512)
    address = models.CharField(default='', max_length=512)
    floor = models.PositiveIntegerField(default=1)
    region = models.CharField(default='', max_length=256)
    partner = models.BooleanField(default=False)
    visit = models.BooleanField(default=False)
    in_person = models.BooleanField(default=False)
    checkout = models.BooleanField(default=False)
    immediate = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)
    def __name__(self):
        return str(self.id)
