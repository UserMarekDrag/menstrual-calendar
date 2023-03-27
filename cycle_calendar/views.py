from django.shortcuts import render, redirect
from datetime import timedelta, datetime, date
from django.utils.safestring import mark_safe
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import calendar
import random
import string

from .forms import UserCalendarForm, UserCalendarDateForm, UniqueTextShareForm, UserShareCalendarForm
from .utils import Calendar
from .models import UserCalendarDate, UserCalendar, UserShareCalendar, UniqueTextShare


def first_visit(request):

    if request.user.is_authenticated:

        users_auth_calendar = UserCalendarDate.objects.filter(user=request.user).values()
        user_auth_calendar = list(users_auth_calendar)

        user_follower = UserShareCalendar.objects.filter(following=request.user).values()
        user_follow_auth = list(user_follower)

        if user_auth_calendar:
            return redirect('calendar')

        elif user_follow_auth:
            return redirect('follow_list')
        else:
            return render(request, 'cycle_calendar/first_visit.html', {'section': 'home', })

    else:
        return render(request, 'cycle_calendar/first_visit.html', {'section': 'home', })


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = UserCalendarDate
    template_name = 'cycle_calendar/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        users_info = UserCalendar.objects.filter(user=self.request.user).values()
        users_info_date = UserCalendarDate.objects.filter(user=self.request.user).values()
        user_auth = list(users_info_date)
        if user_auth:

            today = datetime.today()

            # number of expected cycles
            cycle_list = UserCalendarDate.objects.filter(user=user, start_time__gte=today).count()

            # current cycle
            updates_data = UserCalendarDate.objects.filter(user=user, start_time__lte=today).last()

            user_info = users_info[0]
            user_info_date = updates_data

            # check if the number of cycles and create new ones if is not enough
            if cycle_list < 12:
                update_number_of_cycle(self.request, user_info, user, today, cycle_list)

            context["user_info_date"] = user_info_date
            context["users_info"] = users_info
            context["user_info"] = user_info

        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month, user)
        html_cal = cal.formatmonth(withyear=True)

        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        context["user_auth"] = user_auth

        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


def update_number_of_cycle(request, user_info, user, today, number_of_cycle):
    # user individual parameters
    cycle_length = int(user_info['cycle_length'])
    first_phase_length = int(user_info['first_phase_length'])
    second_phase_length = int(user_info['second_phase_length'])
    third_phase_length = int(user_info['third_phase_length'])

    last_cycle = UserCalendarDate.objects.filter(user=user, start_time__gte=today).values().last()
    start_time = last_cycle['fourth_phase_end']

    # adding one day to the last day of the previous phase
    next_phase = set_new_phase(start_time)

    make_cycle(request, number_of_cycle, next_phase, cycle_length, first_phase_length, second_phase_length,
               third_phase_length)


class CalendarFollowView(LoginRequiredMixin, generic.ListView):
    model = UserCalendarDate
    template_name = 'cycle_calendar/calendar_follow.html'

    def get_context_data(self, **kwargs):
        followed_user = self.kwargs['followed_user']
        context = super().get_context_data(**kwargs)
        users_info = UserCalendar.objects.filter(user_id=followed_user).values()
        users_info_date = UserCalendarDate.objects.filter(user_id=followed_user).values()

        user_auth = list(users_info_date)

        if user_auth:
            today = datetime.today()

            # current cycle
            updates_data = UserCalendarDate.objects.filter(user=followed_user, start_time__lte=today).last()

            user_info = users_info[0]
            user_id = user_info['user_id']
            user_name_list = User.objects.filter(id=user_id)
            user_name = str(user_name_list[0])

            context["user_info_date"] = updates_data
            context["user_info"] = user_info
            context["user_name"] = user_name

        d = get_date_follow(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month, followed_user)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar_follow"] = mark_safe(html_cal)
        context["prev_month_follow"] = prev_month_follow(d)
        context["next_month_follow"] = next_month_follow(d)
        context["user_auth"] = user_auth
        context["followed_user"] = followed_user

        return context


def get_date_follow(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month_follow(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month_follow(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


@login_required
def cycle_info(request):
    users_auth = UserCalendarDate.objects.filter(user=request.user)
    user_auth = list(users_auth)

    users_check = UserCalendar.objects.filter(user=request.user)
    users_check = list(users_check)

    if not users_check:

        if request.method == 'POST':
            form = UserCalendarForm(request.POST)

            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                form.save()
                return redirect('cycle_new')

        else:
            form = UserCalendarForm(instance=request.user)

    else:
        return redirect('cycle_new')

    return render(request, 'cycle_calendar/cycle_info.html', {'form': form,
                                                              'user_auth': user_auth,
                                                              })


@login_required
def update_cycle_info(request):
    users_auth = UserCalendarDate.objects.filter(user=request.user)
    user_auth = list(users_auth)

    cycle_info = UserCalendar.objects.get(user=request.user)
    form = UserCalendarForm(instance=cycle_info)

    if request.method == 'POST':
        form = UserCalendarForm(request.POST, instance=cycle_info)

        if form.is_valid():
            form.save()

            today = datetime.today()

            # current cycle to update
            updates_data = UserCalendarDate.objects.filter(user=request.user, start_time__lte=today).values().last()
            start_time = updates_data['start_time']
            id_update_date = updates_data['id']

            update_record = UserCalendarDate.objects.get(id=id_update_date)

            # delete expected cycles
            delete_date = UserCalendarDate.objects.filter(user=request.user, start_time__gte=today)
            delete_date.delete()

            users_info = UserCalendar.objects.filter(user=request.user).values()
            user_info = users_info[0]

            # user individual parameters
            cycle_length = int(user_info['cycle_length'])
            first_phase_length = int(user_info['first_phase_length'])
            second_phase_length = int(user_info['second_phase_length'])
            third_phase_length = int(user_info['third_phase_length'])

            # changing the data type to mutable
            # formats start_time to a str
            # cycle.start_time format np. 2023-03-12
            first_day_str_list = []

            first_day_str = str(start_time)

            year = int(first_day_str[0:4])
            month = int(first_day_str[5:7])
            day = int(first_day_str[8:])

            first_day_str_list.append(year)
            first_day_str_list.append(month)
            first_day_str_list.append(day)

            first_day_year = first_day_str_list[0]
            first_day_month = first_day_str_list[1]
            first_day_day = first_day_str_list[2]

            # create the current cycle
            first_day = date(first_day_year, first_day_month, first_day_day)
            cycle = Cycle(first_day, cycle_length, first_phase_length, second_phase_length, third_phase_length)
            parameter = cycle.get_list_of_date()

            update_record.first_phase_end = parameter[0]
            update_record.second_phase_start = parameter[1]
            update_record.second_phase_end = parameter[2]
            update_record.third_phase = parameter[3]
            update_record.fourth_phase_start = parameter[4]
            update_record.fourth_phase_end = parameter[5]

            update_record.save()

            # parameter not saved to the database
            next_phase = parameter[6]

            # creating expected cycles
            make_cycle(request, 0, next_phase, cycle_length, first_phase_length, second_phase_length,
                       third_phase_length)

            return redirect('calendar')

    return render(request, 'cycle_calendar/cycle_info.html', {'form': form,
                                                              'user_auth': user_auth,
                                                              })


@login_required
def cycle_add_or_reset_date(request):
    users_auth = UserCalendarDate.objects.filter(user=request.user)
    user_auth = list(users_auth)

    if request.method == 'POST':

        users_info = UserCalendar.objects.filter(user=request.user).values()
        user_info = users_info[0]

        # user individual parameters
        cycle_length = int(user_info['cycle_length'])
        first_phase_length = int(user_info['first_phase_length'])
        second_phase_length = int(user_info['second_phase_length'])
        third_phase_length = int(user_info['third_phase_length'])

        form = UserCalendarDateForm(request.POST)

        if form.is_valid():

            cycle_form = form.save(commit=False)
            cycle_form.user = request.user

            if user_auth:
                today = datetime.today()

                # delete current cycle
                updates_data = UserCalendarDate.objects.filter(user=request.user, start_time__lte=today).last()
                updates_data.delete()

                # delete expected cycles
                delete_date = UserCalendarDate.objects.filter(user=request.user, start_time__gte=today)
                delete_date.delete()

            # changing the data type to mutable
            # formats start_time to a str
            # cycle_form.start_time format np. 2023-03-12
            first_day_str_list = []

            first_day_str = str(cycle_form.start_time)

            year = int(first_day_str[0:4])
            month = int(first_day_str[5:7])
            day = int(first_day_str[8:])

            first_day_str_list.append(year)
            first_day_str_list.append(month)
            first_day_str_list.append(day)

            first_day_year = first_day_str_list[0]
            first_day_month = first_day_str_list[1]
            first_day_day = first_day_str_list[2]

            # create the current cycle_form
            first_day = date(first_day_year, first_day_month, first_day_day)
            cycle = Cycle(first_day, cycle_length, first_phase_length, second_phase_length, third_phase_length)
            parameter = cycle.get_list_of_date()

            cycle_form.first_phase_end = parameter[0]
            cycle_form.second_phase_start = parameter[1]
            cycle_form.second_phase_end = parameter[2]
            cycle_form.third_phase = parameter[3]
            cycle_form.fourth_phase_start = parameter[4]
            cycle_form.fourth_phase_end = parameter[5]

            cycle_form.save()

            # parameter not saved to the database
            next_phase = parameter[6]

            # creating expected cycles
            make_cycle(request, 0, next_phase, cycle_length, first_phase_length, second_phase_length,
                       third_phase_length)

            return redirect('calendar')

    else:
        form = UserCalendarDateForm()

    return render(request, 'cycle_calendar/cycle_new.html', {'form': form,
                                                             'user_auth': user_auth,
                                                             })


def make_cycle(request, cycle_num, first_day, cycle_length, first_phase_length, second_phase_length,
               third_phase_length):
    # checking the number of expected cycles
    if not cycle_num == 12:

        form = UserCalendarDateForm(request.POST)
        cycle_form = form.save(commit=False)
        cycle_form.user = request.user

        cycle_form.start_time = first_day

        cycle = Cycle(first_day, cycle_length, first_phase_length, second_phase_length, third_phase_length)

        parameter = cycle.get_list_of_date()
        cycle_form.first_phase_end = parameter[0]
        cycle_form.second_phase_start = parameter[1]
        cycle_form.second_phase_end = parameter[2]
        cycle_form.third_phase = parameter[3]
        cycle_form.fourth_phase_start = parameter[4]
        cycle_form.fourth_phase_end = parameter[5]

        cycle_form.save()

        next_phase = parameter[6]

        make_cycle(request, cycle_num + 1, next_phase, cycle_length, first_phase_length, second_phase_length,
                   third_phase_length)

    else:
        return


class Cycle:

    def __init__(self, first_day, cycle_length, first_phase_length, second_phase_length, third_phase_length):
        self.first_day = first_day
        self.cycle_length = cycle_length
        self.first_phase_length = first_phase_length
        self.second_phase_length = second_phase_length
        self.third_phase_length = third_phase_length
        self.phase_list = []

    # calculate dates and add items to lists
    def set_cycle_date(self):
        first_phase_end = set_end_phase(self.first_day, self.first_phase_length)
        self.phase_list.append(first_phase_end)

        second_phase_start = set_new_phase(first_phase_end)
        self.phase_list.append(second_phase_start)

        second_phase_end = set_end_phase(second_phase_start, self.second_phase_length)
        self.phase_list.append(second_phase_end)

        third_phase = set_new_phase(second_phase_end)
        self.phase_list.append(third_phase)

        fourth_phase_start = set_new_phase(third_phase)
        self.phase_list.append(fourth_phase_start)

        fourth_phase_length = self.cycle_length - self.first_phase_length - self.second_phase_length - self.third_phase_length

        fourth_phase_end = set_end_phase(fourth_phase_start, fourth_phase_length)
        self.phase_list.append(fourth_phase_end)

        next_phase = set_new_phase(fourth_phase_end)
        self.phase_list.append(next_phase)

    def get_list_of_date(self):
        self.set_cycle_date()
        return self.phase_list


def set_new_phase(end_date_previous_phase):
    start_phase = (end_date_previous_phase + timedelta(days=1))
    return start_phase


def set_end_phase(start_phase, length_phase):
    end_phase = (start_phase + timedelta(days=length_phase - 1))
    return end_phase


def generate_random_string(length=15):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@login_required
def share_unique_text(request):
    users_auth = UserCalendarDate.objects.filter(user=request.user)
    user_auth = list(users_auth)

    # empty variables
    text = ''
    last_text = ''
    text_auth = False

    if request.method == 'POST':
        form = UniqueTextShareForm(request.POST)

        prev_unique_text = UniqueTextShare.objects.filter(user_sharing=request.user)
        prev_unique_text.delete()

        post = form.save(commit=False)
        post.unique_text = generate_random_string()
        post.user_sharing = request.user
        form.save()
        text = UniqueTextShare.objects.filter(user_sharing=request.user).values().order_by('-created_date')
        last_text = text[0]

        text_auth = list(text)

    else:
        form = UniqueTextShareForm(instance=request.user)

    return render(request, 'cycle_calendar/cycle_share.html', {'form': form,
                                                               'user_auth': user_auth,
                                                               'text': text,
                                                               'last_text': last_text,
                                                               'text_auth': text_auth,
                                                               })


@login_required
def check_unique_text(request):
    user_follower = UserShareCalendar.objects.filter(following=request.user).values()
    user_follow_auth = list(user_follower)

    # last add unique text
    text = UniqueTextShare.objects.filter().values().order_by('-created_date')

    # empty variables
    error_info = ''

    if request.method == 'POST':
        form = UniqueTextShareForm(request.POST)
        form_share = UserShareCalendarForm()

        if form.is_valid():

            for i in text:
                unique_text = i['unique_text']
                user_id = i['user_sharing_id']
                user_name_list = User.objects.filter(id=user_id)
                user_name = user_name_list[0]

                if request.POST['unique_text'] == str(unique_text):
                    users_connect = form_share.save(commit=False)

                    users_connect.following = request.user
                    users_connect.user = user_name
                    users_connect.save()

                    unique_text_to_del = UniqueTextShare.objects.filter(unique_text=unique_text)
                    unique_text_to_del.delete()

                    return redirect('follow_list')
                else:
                    error_info = 'The code is incorrect, try again.'

    else:
        form = UniqueTextShareForm()

    return render(request, 'cycle_calendar/cycle_share_check.html', {'form': form,
                                                                     'text': text,
                                                                     'error_info': error_info,
                                                                     'user_follower': user_follower,
                                                                     'user_follow_auth': user_follow_auth,
                                                                     })


@login_required
def follow_list(request):
    user_follower = UserShareCalendar.objects.filter(following=request.user).values()
    user_name_list = User.objects.filter()
    user_follow_auth = list(user_follower)

    return render(request, 'cycle_calendar/follow_list.html', {'user_follow_auth': user_follow_auth,
                                                               'user_name_list': user_name_list,
                                                               'user_follower': user_follower,
                                                               })


@login_required
def share_list(request):
    user_follower = UserShareCalendar.objects.filter(user=request.user).values()
    user_name_list = User.objects.filter()
    user_follow_auth = list(user_follower)

    return render(request, 'cycle_calendar/share_list.html', {'user_follow_auth': user_follow_auth,
                                                              'user_name_list': user_name_list,
                                                              'user_follower': user_follower,
                                                              })


@login_required
def delete_user_from_share_list(request, pk):
    user_follower = UserShareCalendar.objects.filter(id=pk)
    user_follower.delete()

    return redirect('share_list')
