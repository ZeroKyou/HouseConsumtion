from meter.models import Electricity
from django.utils import timezone
import json
import time


class ElectricityGraphData(object):

    def get_data(self, time_period, cost_kw_h):
        '''
        Fetches energy readings from the db and returns them in a json string.
        :param time_period: Period of time when the wanted readings were stored.
        :param cost_kw_h: Cost of 1 kilowatt per hour.
        :return: serialized dictionary as a json string with the wanted readings (voltage, power, etc.)
        '''

        if time_period == "year":
            return json.dumps(self.__get_data_year(cost_kw_h))
        if time_period == "month":
            return json.dumps(self.__get_data_month(cost_kw_h))
        elif time_period == "actual":
            return json.dumps(self.__get_data_actual(cost_kw_h))

    def __get_data_year(self, cost_kw_h):
        '''
        Fetches the averages of each reading for each month of the year and returns them in a json string.
        :param data: Dictionary used to store the fetched values.
        :return: serialized dictionary as a json string with the wanted averages (voltage, power, etc.)
        '''
        # USE START_DATE AS BEGINNING OF WANTED MONTH AND END_DATE AS BEGINNING OF NEXT MONTH
        # USER date__range_gte=(START_DATE).date_range_lt=(END_DATE)
        data = {
            'voltage': [],
            'current': [],
            'power': [],
            'avg_v': [],
            'avg_c': [],
            'avg_p': [],
            'cost': [],
        }
        current_date = timezone.datetime.now()
        start_date = timezone.datetime(current_date.year, 1, 1)
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
        for month in range(1, current_date.month + 1):
            end_date = timezone.datetime(current_date.year, month + 1, 1)
            end_date = timezone.make_aware(end_date, timezone.get_default_timezone())
            current = Electricity.objects.get_avg_current(start_date, end_date)
            voltage = Electricity.objects.get_avg_voltage(start_date, end_date)
            power = Electricity.objects.get_avg_power(start_date, end_date)
            data['current'].append(current)
            data['voltage'].append(voltage)
            data['power'].append(power)
            start_date = end_date

        start_date = timezone.datetime(current_date.year, 1, 1)
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
        current_date = timezone.make_aware(current_date, timezone.get_default_timezone())
        data['avg_v'].append(Electricity.objects.get_avg_voltage(start_date, current_date))
        data['avg_c'].append(Electricity.objects.get_avg_current(start_date, current_date))
        data['avg_p'].append(Electricity.objects.get_avg_power(start_date, current_date))
        data['cost'].append(Electricity.objects.get_cost(cost_kw_h, start_date, current_date))

        return data

    def __get_data_month(self, cost_kw_h):
        '''
        Fetches the averages of each reading for each day of the last 30 days and returns them in a json string.
        :param data: Dictionary used to store the fetched values.
        :return: serialized dictionary as a json string with the wanted averages (voltage, power, etc.)
        '''
        data = {
            'voltage': [],
            'current': [],
            'power': [],
            'avg_v': [],
            'avg_c': [],
            'avg_p': [],
            'cost': [],
        }
        # hours = 0
        current_date = timezone.datetime.now()
        one_day = timezone.timedelta(1)
        thirty_days_ago = timezone.timedelta(-30)
        start_date = current_date + thirty_days_ago
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
        end_date = start_date

        for day in range(1, 31):
            start_date_js = int(time.mktime(start_date.timetuple())) * 1000
            end_date = end_date + one_day
            current = Electricity.objects.get_avg_current(start_date, end_date)
            voltage = Electricity.objects.get_avg_voltage(start_date, end_date)
            power = Electricity.objects.get_avg_power(start_date, end_date)
            # get hours between first reading and last reading and add them
            # hours += n_hours
            current = [start_date_js, current]
            voltage = [start_date_js, voltage]
            power = [start_date_js, power]
            data['current'].append(current)
            data['voltage'].append(voltage)
            data['power'].append(power)
            start_date = end_date

        start_date = current_date + thirty_days_ago
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
        current_date = timezone.make_aware(current_date, timezone.get_default_timezone())
        data['avg_v'].append(Electricity.objects.get_avg_voltage(start_date, current_date))
        data['avg_c'].append(Electricity.objects.get_avg_current(start_date, current_date))
        data['avg_p'].append(Electricity.objects.get_avg_power(start_date, current_date))
        data['cost'].append(Electricity.objects.get_cost(cost_kw_h, start_date, current_date))
        # data['cost'].append(Electricity.objects.get_cost(cost_kw_h, hours))

        return data

    def __get_data_actual(self, cost_kw_h):
        '''
        Fetches the averages of each reading for each day of the last 30 days and returns them in a json string.
        :param data: Dictionary used to store the fetched values.
        :return: serialized dictionary as a json string with the wanted averages (voltage, power, etc.)
        '''
        data = {
            'voltage': [],
            'current': [],
            'power': [],
            'avg_v': [],
            'avg_c': [],
            'avg_p': [],
            'cost': [],
        }
        # hours = 0
        one_hour = timezone.datetime(2000, 1, 1, 2) - timezone.datetime(2000, 1, 1, 1)
        current_date = timezone.datetime.now()
        start_date = current_date - one_hour
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())

        results = Electricity.objects.filter(date__gte=start_date, date__lte=timezone.now())

        if not results.exists():
            return data

        for result in results:
            date_js = int(time.mktime(result.date.timetuple())) * 1000
            current = [date_js, result.current]
            voltage = [date_js, result.voltage]
            power = [date_js, round(result.power, 2)]
            data['current'].append(current)
            data['voltage'].append(voltage)
            data['power'].append(power)

        start_date = current_date - one_hour
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
        current_date = timezone.make_aware(current_date, timezone.get_default_timezone())
        data['avg_v'].append(Electricity.objects.get_avg_voltage(start_date, current_date))
        data['avg_c'].append(Electricity.objects.get_avg_current(start_date, current_date))
        data['avg_p'].append(Electricity.objects.get_avg_power(start_date, current_date))
        data['cost'].append(Electricity.objects.get_cost(cost_kw_h, start_date, current_date))

        return data



