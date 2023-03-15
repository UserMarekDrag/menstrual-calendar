from django.contrib import admin
from .models import UserCalendar, UserCalendarDate, UserShareCalendar, UniqueTextShare

admin.site.register(UserCalendar)
admin.site.register(UserCalendarDate)
admin.site.register(UserShareCalendar)
admin.site.register(UniqueTextShare)
