from django.db import models
from django.conf import settings
from django.utils import timezone


class UserCalendar(models.Model):
    FIRST_PHASE_LENGTH_CHOICE = (
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
    )

    CYCLE_LENGTH_CHOICE = (
        ("25", "25"),
        ("26", "26"),
        ("27", "27"),
        ("28", "28"),
        ("29", "29"),
        ("30", "30"),
        ("31", "31"),
        ("32", "32"),
        ("33", "33"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cycle_length = models.CharField(max_length=20, choices=CYCLE_LENGTH_CHOICE, default='28')
    first_phase_length = models.CharField(max_length=20, choices=FIRST_PHASE_LENGTH_CHOICE, default='5')
    second_phase_length = models.IntegerField(default=8)
    third_phase_length = models.IntegerField(default=1)


class UserCalendarDate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateField(blank=True, null=True)
    first_phase_end = models.DateField(blank=True, null=True)
    second_phase_start = models.DateField(blank=True, null=True)
    second_phase_end = models.DateField(blank=True, null=True)
    third_phase = models.DateField(blank=True, null=True)
    fourth_phase_start = models.DateField(blank=True, null=True)
    fourth_phase_end = models.DateField(blank=True, null=True)


class UserShareCalendar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followed_by', on_delete=models.CASCADE)


class UniqueTextShare(models.Model):
    user_sharing = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unique_text = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
