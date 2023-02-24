from django.db import models
from django.conf import settings


class Profile(models.Model):

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICE = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default=FEMALE)

    def __str__(self):
        return 'Profil użytkownika {}.'.format(self.user.username)
