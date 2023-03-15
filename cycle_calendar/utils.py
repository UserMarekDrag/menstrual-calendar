from calendar import HTMLCalendar
from .models import UserCalendarDate


# test
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, user=None):
        self.year = year
        self.month = month
        self.user = user
        super(Calendar, self).__init__()

        self.first_phase = False
        self.second_phase = False
        self.fourth_phase = False
        self.change_phase = False

    # formats a day as a td
    # filter events by day
    def formatday(self, day, cycle_start_and_end, cycle_start, cycle_end):

        # check if the day is in cycle which is end in this month
        end_first_phase_days = cycle_end.filter(start_time__day=day, start_time__month=self.month, start_time__year=self.year)
        end_first_phase_end = cycle_end.filter(first_phase_end__day=day, first_phase_end__month=self.month, first_phase_end__year=self.year)
        end_second_phase_start = cycle_end.filter(second_phase_start__day=day, second_phase_start__month=self.month, second_phase_start__year=self.year)
        end_second_phase_end = cycle_end.filter(second_phase_end__day=day, second_phase_end__month=self.month, second_phase_end__year=self.year)
        end_third_phase = cycle_end.filter(third_phase__day=day, third_phase__month=self.month, third_phase__year=self.year)
        end_fourth_phase_start = cycle_end.filter(fourth_phase_start__day=day, fourth_phase_start__month=self.month, fourth_phase_start__year=self.year)
        end_fourth_phase_end = cycle_end.filter(fourth_phase_end__day=day, fourth_phase_end__month=self.month, fourth_phase_end__year=self.year)

        # check if the day is in cycle which is all in this month
        all_first_phase_days = cycle_start_and_end.filter(start_time__day=day, start_time__month=self.month, start_time__year=self.year)
        all_first_phase_end = cycle_start_and_end.filter(first_phase_end__day=day, first_phase_end__month=self.month, first_phase_end__year=self.year)
        all_second_phase_start = cycle_start_and_end.filter(second_phase_start__day=day, second_phase_start__month=self.month, second_phase_start__year=self.year)
        all_second_phase_end = cycle_start_and_end.filter(second_phase_end__day=day, second_phase_end__month=self.month, second_phase_end__year=self.year)
        all_third_phase = cycle_start_and_end.filter(third_phase__day=day, third_phase__month=self.month, third_phase__year=self.year)
        all_fourth_phase_start = cycle_start_and_end.filter(fourth_phase_start__day=day, fourth_phase_start__month=self.month, fourth_phase_start__year=self.year)
        all_fourth_phase_end = cycle_start_and_end.filter(fourth_phase_end__day=day, fourth_phase_end__month=self.month, fourth_phase_end__year=self.year)

        # check if the day is in cycle which is start in this month
        start_first_phase_days = cycle_start.filter(start_time__day=day, start_time__month=self.month, start_time__year=self.year)
        start_first_phase_end = cycle_start.filter(first_phase_end__day=day, first_phase_end__month=self.month, first_phase_end__year=self.year)
        start_second_phase_start = cycle_start.filter(second_phase_start__day=day, second_phase_start__month=self.month, second_phase_start__year=self.year)
        start_second_phase_end = cycle_start.filter(second_phase_end__day=day, second_phase_end__month=self.month, second_phase_end__year=self.year)
        start_third_phase = cycle_start.filter(third_phase__day=day, third_phase__month=self.month, third_phase__year=self.year)
        start_fourth_phase_start = cycle_start.filter(fourth_phase_start__day=day, fourth_phase_start__month=self.month, fourth_phase_start__year=self.year)
        start_fourth_phase_end = cycle_start.filter(fourth_phase_end__day=day, fourth_phase_end__month=self.month, fourth_phase_end__year=self.year)

        if end_first_phase_days or all_first_phase_days or start_first_phase_days:
            self.first_phase = True
            self.change_phase = True

        elif end_first_phase_end or all_first_phase_end or start_first_phase_end:
            self.first_phase = False
            self.change_phase = True

        elif end_second_phase_start or all_second_phase_start or start_second_phase_start:
            self.second_phase = True
            self.change_phase = True

        elif end_second_phase_end or all_second_phase_end or start_second_phase_end:
            self.second_phase = False
            self.change_phase = True

        elif end_third_phase or all_third_phase or start_third_phase:
            self.change_phase = True

        elif end_fourth_phase_start or all_fourth_phase_start or start_fourth_phase_start:
            self.fourth_phase = True
            self.change_phase = True

        elif end_fourth_phase_end or all_fourth_phase_end or start_fourth_phase_end:
            self.fourth_phase = False
            self.change_phase = True

        if day != 0:

            # check if the first days of the month are not a continuation of the cycle phase in prev month
            if not self.change_phase:
                for i in range(1, 17):

                    end_first_phase_end = cycle_end.filter(first_phase_end__day=i, first_phase_end__month=self.month, first_phase_end__year=self.year,)
                    end_second_phase_end = cycle_end.filter(second_phase_end__day=i, second_phase_end__month=self.month, second_phase_end__year=self.year)
                    end_fourth_phase_end = cycle_end.filter(fourth_phase_end__day=i, fourth_phase_end__month=self.month, fourth_phase_end__year=self.year)

                    if end_first_phase_end:
                        self.first_phase = True
                        break
                    if end_second_phase_end:
                        self.second_phase = True
                        break
                    if end_fourth_phase_end:
                        self.fourth_phase = True
                        break

            if self.first_phase or end_first_phase_end or all_first_phase_end or start_first_phase_end:

                return f"<td class='cal-td-phase-first'><div span='date'>{day}</span><ul></ul></td>"

            elif self.second_phase or end_second_phase_end or all_second_phase_end or start_second_phase_end:

                return f"<td class='cal-td-phase-second'><div span='date'>{day}</span><ul></ul></td>"

            elif end_third_phase or all_third_phase or start_third_phase:

                return f"<td class='cal-td-phase-third'><div span='date'>{day}</span><ul></ul></td>"

            elif self.fourth_phase or end_fourth_phase_end or all_fourth_phase_end or start_fourth_phase_end:

                return f"<td class='cal-td-phase-fourth'><div span='date'>{day}</span><ul></ul></td>"

            else:
                return f"<td class='cal-td-basic'><div span='date'>{day}</span><ul></ul></td>"

        return "<td class='cal-td-basic'></td>"

    # formats a week as a tr
    def formatweek(self, the_week, cycle_start_and_end, cycle_start, cycle_end):
        week = ""
        for d, weekday in the_week:
            week += self.formatday(d, cycle_start_and_end, cycle_start, cycle_end)
        return f"<tr> {week} </tr>"

    # formats a month as a table
    # filter events by year, month and user
    def formatmonth(self, withyear=True):

        add_month = self.month + 1
        sub_month = self.month - 1

        if add_month == 13:
            add_month = 1

        if sub_month == 0:
            sub_month = 12

        # cycle start and end in actual month
        cycle_start_and_end = UserCalendarDate.objects.filter(
            start_time__year=self.year,
            start_time__month=self.month,
            fourth_phase_end__month=self.month,
            user=self.user)

        # cycle start in actual month and end in next month
        cycle_start = UserCalendarDate.objects.filter(
            start_time__year=self.year,
            start_time__month=self.month,
            fourth_phase_end__month=add_month,
            user=self.user)

        # cycle start in prev month and end in actual month
        cycle_end = UserCalendarDate.objects.filter(
            start_time__year=self.year,
            start_time__month=sub_month,
            fourth_phase_end__month=self.month,
            user=self.user)

        cal = ('<table align="center" cellspacing="0" cellpadding="21" class="calendar">\n')  # noqa
        cal += (f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n")  # noqa
        cal += f"{self.formatweekheader()}\n"

        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, cycle_start_and_end, cycle_start, cycle_end)}\n"
        return cal + '</table>'
