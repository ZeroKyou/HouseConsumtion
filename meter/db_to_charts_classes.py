from meter.models import Electricity
from django.utils import timezone


class ElectricityGraphData:

    @staticmethod
    def get_data(time_period):
        data = {'': []}
        current_date = timezone.now()

        if time_period == 'year':
            start_date = current_date + timezone.timedelta(days=-365)   # one year ago
            results = Electricity.objects.filter(date__range=(start_date, current_date)).orderby('date')
        elif time_period == 'month':
            start_date = current_date + timezone.timedelta(days=-30)    # one month ago
            results = Electricity.objects.filter(date__range=(start_date, current_date)).orderby('date')
        else:
            start_date = current_date + timezone.timedelta(days=-1)     # one day ago
            results = Electricity.objects.filter(date__range=(start_date, current_date)).orderby('date')

        if not results.exists():
            return None

        for result in results:
            data['current'].append(result.current)
            data['voltage'].append(result.voltage)
            data['power'].append(result.power)
            data['date'].append(result.date)
        return data


