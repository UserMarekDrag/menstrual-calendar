# Generated by Django 4.1.5 on 2023-03-06 00:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cycle_calendar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercalendar',
            name='start_time',
        ),
        migrations.CreateModel(
            name='UserCalendarDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
