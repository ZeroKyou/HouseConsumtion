from django.db.models import Manager, Avg


class ElectricityManager(Manager):

    def get_avg_current(self, start_date, end_date):
        avg_current = self.filter(date__gte=start_date, date__lt=end_date).aggregate(Avg('current'))
        if avg_current['current__avg'] is None:
            return 0
        return round(avg_current['current__avg'], 2)

    def get_avg_voltage(self, start_date, end_date):
        avg_voltage = self.filter(date__gte=start_date, date__lt=end_date).aggregate(Avg('voltage'))
        if avg_voltage['voltage__avg'] is None:
            return 0
        return avg_voltage['voltage__avg']

    def get_avg_power(self, start_date, end_date):
        avg_power = 0
        results = self.filter(date__gte=start_date, date__lt=end_date)

        if not results.exists():
            return 0

        for result in results:
            avg_power += result.power

        return round(avg_power/len(results), 2)

    def get_cost(self, cost_kw_h, start_date, end_date):
        avg_power = self.get_avg_power(start_date, end_date)
        results = self.filter(date__gte=start_date, date__lt=end_date)
        date_first_reading = results.first().date
        date_last_reading = results.last().date
        hours = date_last_reading - date_first_reading
        hours = max(1, float(hours.total_seconds()) / 3600)
        avg_power_kw = float(avg_power)/1000
        cost = hours * avg_power_kw * cost_kw_h
        return round(cost, 2)
