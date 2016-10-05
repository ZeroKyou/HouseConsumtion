from meter.models import Electricity
from django.utils import timezone
import json


class ElectricityGraphData(object):

    @staticmethod
    def get_data(time_period):
        data = {
            'voltage': [],
            'current': [],
            'power': [],
            'date': [],
            'avg_v': [],
            'avg_c': [],
            'avg_p': [],
            'cost': [],
        }
        current_date = timezone.now()

        if time_period == "year":
            start_date = current_date + timezone.timedelta(days=-365)   # one year ago
        elif time_period == "month":
            start_date = current_date + timezone.timedelta(days=-30)    # one month ago
        elif time_period == "day":
            start_date = current_date + timezone.timedelta(days=-1)     # one day ago

        results = Electricity.objects.filter(date__range=(start_date, current_date)).order_by('date')

        if not results.exists():
            return json.dumps([])

        data['avg_v'].append(Electricity.objects.get_avg_voltage(time_period))
        data['avg_c'].append(Electricity.objects.get_avg_current(time_period))
        data['avg_p'].append(Electricity.objects.get_avg_power(time_period))
        data['cost'].append(Electricity.objects.get_cost(0, time_period))

        for result in results:
            data['voltage'].append(result.voltage)
            data['current'].append(result.current)
            data['power'].append(round(result.power, 2))
            data['date'].append(result.date.isoformat())

        return json.dumps(data)

# class ElectricityGraphData(object):
#
#     @staticmethod
#     def get_data(time_period):
#         data = {'current': [],
#                 'voltage': [],
#                 'power': [],
#                 'date': []}
#         current_date = timezone.now()
#
#         if time_period == "year":
#             start_date = current_date + timezone.timedelta(days=-365)   # one year ago
#             results = Electricity.objects.filter(date__range=(start_date, current_date)).order_by('date')
#         elif time_period == "month":
#             start_date = current_date + timezone.timedelta(days=-30)    # one month ago
#             results = Electricity.objects.filter(date__range=(start_date, current_date)).order_by('date')
#         elif time_period == "day":
#             start_date = current_date + timezone.timedelta(days=-1)     # one day ago
#             results = Electricity.objects.filter(date__range=(start_date, current_date)).order_by('date')
#
#         if not results.exists():
#             return None
#
#         for result in results:
#             data['current'].append(result.current)
#             data['voltage'].append(result.voltage)
#             data['power'].append(round(result.power, 2))
#             data['date'].append(result.date)
#         return data


