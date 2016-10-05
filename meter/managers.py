from django.db.models import Manager, Avg
from django.utils import timezone


class ElectricityManager(Manager):

    def get_avg_current(self, time_period="month"):

        current_date = timezone.now()

        if time_period == "year":
            start_date = current_date + timezone.timedelta(days=-365)  # one year ago
        elif time_period == "month":
            start_date = current_date + timezone.timedelta(days=-30)  # one month ago
        elif time_period == "day":
            start_date = current_date + timezone.timedelta(days=-1)  # one day ago

        avg_current = self.filter(date__range=(start_date, current_date)).aggregate(Avg('current'))

        return round(avg_current['current__avg'], 2)

    def get_avg_voltage(self, time_period="month"):

        current_date = timezone.now()

        if time_period == "year":
            start_date = current_date + timezone.timedelta(days=-365)   # one year ago
        elif time_period == "month":
            start_date = current_date + timezone.timedelta(days=-30)    # one month ago
        elif time_period == "day":
            start_date = current_date + timezone.timedelta(days=-1)     # one day ago

        avg_voltage = self.filter(date__range=(start_date, current_date)).aggregate(Avg('voltage'))

        return avg_voltage['voltage__avg']

    def get_avg_power(self, time_period="month"):

        current_date = timezone.now()
        avg_power = 0

        if time_period == "year":
            start_date = current_date + timezone.timedelta(days=-365)  # one year ago
        elif time_period == "month":
            start_date = current_date + timezone.timedelta(days=-30)  # one month ago
        elif time_period == "day":
            start_date = current_date + timezone.timedelta(days=-1)  # one day ago

        results = self.filter(date__range=(start_date, current_date))

        for result in results:
            avg_power += result.power

        return round(avg_power, 2)

    def get_cost(self, cost_kw_h, time_period="month"):

        avg_power = self.get_avg_power(time_period)

        if time_period == "year":
            hours = 365 * 24
        elif time_period == "month":
            hours = 30 * 24
        elif time_period == "day":
            hours = 24

        avg_power_kw = avg_power/1000
        cost = avg_power_kw*hours*cost_kw_h

        return round(cost, 2)
