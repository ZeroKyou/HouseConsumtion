from meter.models import Electricity, Water
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
        else:
            return json.dumps(self.__get_data_actual(cost_kw_h))

    def __get_data_year(self, cost_kw_h):
        '''
        Fetches the averages of each reading of each month of the year and returns them in a json string.
        :param cost_kw_h: Cost of 1 kilowatt per hour.
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
        avg_v = Electricity.objects.get_avg_voltage(start_date, current_date)
        avg_c = Electricity.objects.get_avg_current(start_date, current_date)
        avg_p = Electricity.objects.get_avg_power(start_date, current_date)
        cost = Electricity.objects.get_cost(cost_kw_h, start_date, current_date)

        if (avg_v is not None) and (avg_c is not None) and (avg_p is not None) and (cost is not None):
            data['avg_v'].append(avg_v)
            data['avg_c'].append(avg_c)
            data['avg_p'].append(avg_p)
            data['cost'].append(cost)

        return data

    def __get_data_month(self, cost_kw_h):
        '''
        Fetches the averages of each reading of each day of the last 30 days and returns them in a json string.
        :param cost_kw_h: Cost of 1 kilowatt per hour.
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
        current_date = timezone.datetime.now()
        one_day = timezone.timedelta(1)
        thirty_days_ago = timezone.timedelta(-30)
        start_date = current_date + thirty_days_ago
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
        end_date = start_date

        for day in range(1, 32):
            start_date_js = int(time.mktime(start_date.timetuple())) * 1000
            end_date = end_date + one_day
            current = Electricity.objects.get_avg_current(start_date, end_date)
            voltage = Electricity.objects.get_avg_voltage(start_date, end_date)
            power = Electricity.objects.get_avg_power(start_date, end_date)
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
        avg_v = Electricity.objects.get_avg_voltage(start_date, current_date)
        avg_c = Electricity.objects.get_avg_current(start_date, current_date)
        avg_p = Electricity.objects.get_avg_power(start_date, current_date)
        cost = Electricity.objects.get_cost(cost_kw_h, start_date, current_date)

        if (avg_v is not None) and (avg_c is not None) and (avg_p is not None) and (cost is not None):
            data['avg_v'].append(avg_v)
            data['avg_c'].append(avg_c)
            data['avg_p'].append(avg_p)
            data['cost'].append(cost)

        return data

    def __get_data_actual(self, cost_kw_h):
        '''
        Fetches the averages of each reading of the past one hour and returns them in a json string.
        :param cost_kw_h: Cost of 1 kilowatt per hour.
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
        avg_v = Electricity.objects.get_avg_voltage(start_date, current_date)
        avg_c = Electricity.objects.get_avg_current(start_date, current_date)
        avg_p = Electricity.objects.get_avg_power(start_date, current_date)
        cost = Electricity.objects.get_cost(cost_kw_h, start_date, current_date)

        if (avg_v is not None) and (avg_c is not None) and (avg_p is not None) and (cost is not None):
            data['avg_v'].append(avg_v)
            data['avg_c'].append(avg_c)
            data['avg_p'].append(avg_p)
            data['cost'].append(cost)

        return data


class WaterGraphData(object):

    def get_data(self, time_period, cost_m3):
        '''
        Fetches water readings from the db and returns them in a json string.
        :param time_period: Period of time when the wanted readings were stored.
        :param cost_m3: Cost of 1 cubic meter of water.
        :return: serialized dictionary as a json string with the wanted readings (cubic meters and liters of water)
        '''

        if time_period == "year":
            return json.dumps(self.__get_data_year(cost_m3))
        if time_period == "month":
            return json.dumps(self.__get_data_month(cost_m3))
        else:
            return json.dumps(self.__get_data_actual(cost_m3))

    def __get_data_year(self, cost_m3):
        '''
        Fetches the total readings of each month of the year and returns them in a json string.
        :param cost_m3: Cost of 1 cubic meter of water.
        :return: serialized dictionary as a json string with the wanted readings (cubic meters and liters of water)
        '''
        data = {
            'liters': [],
            'cubic_meters': [],
            'total_l': [],
            'total_m3': [],
            'cost': [],
        }
        current_date = timezone.datetime.now()
        start_date = timezone.datetime(current_date.year, 1, 1)
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
        for month in range(1, current_date.month + 1):
            end_date = timezone.datetime(current_date.year, month + 1, 1)
            end_date = timezone.make_aware(end_date, timezone.get_default_timezone())
            liters = Water.objects.get_total_liters(start_date, end_date)
            cubic_meters = Water.objects.get_total_m3(start_date, end_date)
            data['liters'].append(liters)
            data['cubic_meters'].append(cubic_meters)
            start_date = end_date

        start_date = timezone.datetime(current_date.year, 1, 1)
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
        current_date = timezone.make_aware(current_date, timezone.get_default_timezone())
        total_l = Water.objects.get_total_liters(start_date, current_date)
        total_m3 = Water.objects.get_total_m3(start_date, current_date)
        cost = Water.objects.get_cost(cost_m3, start_date, current_date)

        if (total_l is not None) and (total_m3 is not None) and (cost is not None):
            data['total_l'].append(Water.objects.get_total_liters(start_date, current_date))
            data['total_m3'].append(Water.objects.get_total_m3(start_date, current_date))
            data['cost'].append(Water.objects.get_cost(cost_m3, start_date, current_date))

        return data

    def __get_data_month(self, cost_m3):
        '''
        Fetches the liters and cubic meters of water for each day of the last 30 days and returns them
        in a json string.
        :param cost_m3: Cost of 1 cubic meter of water.
        :return: serialized dictionary as a json string with the wanted readings (cubic meters and liters of water)
        '''
        data = {
            'liters': [],
            'cubic_meters': [],
            'total_l': [],
            'total_m3': [],
            'cost': [],
        }
        current_date = timezone.datetime.now()
        one_day = timezone.timedelta(1)
        thirty_days_ago = timezone.timedelta(-30)
        start_date = current_date + thirty_days_ago
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
        end_date = start_date

        for day in range(1, 32):
            start_date_js = int(time.mktime(start_date.timetuple())) * 1000
            end_date = end_date + one_day
            liters = Water.objects.get_total_liters(start_date, end_date)
            cubic_meters = Water.objects.get_total_m3(start_date, end_date)
            liters = [start_date_js, liters]
            cubic_meters = [start_date_js, cubic_meters]
            data['liters'].append(liters)
            data['cubic_meters'].append(cubic_meters)
            start_date = end_date

        start_date = current_date + thirty_days_ago
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
        current_date = timezone.make_aware(current_date, timezone.get_default_timezone())
        total_l = Water.objects.get_total_liters(start_date, current_date)
        total_m3 = Water.objects.get_total_m3(start_date, current_date)
        cost = Water.objects.get_cost(cost_m3, start_date, current_date)

        if (total_l is not None) and (total_m3 is not None) and (cost is not None):
            data['total_l'].append(Water.objects.get_total_liters(start_date, current_date))
            data['total_m3'].append(Water.objects.get_total_m3(start_date, current_date))
            data['cost'].append(Water.objects.get_cost(cost_m3, start_date, current_date))

        return data

    def __get_data_actual(self, cost_m3):
        '''
        Fetches the liters and cubic meters of water of the past 1 hour and returns them
        in a json string.
        :param cost_m3: Cost of 1 cubic meter of water.
        :return: serialized dictionary as a json string with the wanted readings (cubic meters and liters of water)
        '''
        data = {
            'liters': [],
            'cubic_meters': [],
            'total_l': [],
            'total_m3': [],
            'cost': [],
        }
        one_hour = timezone.datetime(2000, 1, 1, 2) - timezone.datetime(2000, 1, 1, 1)
        current_date = timezone.datetime.now()
        start_date = current_date - one_hour
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())

        results = Water.objects.filter(date__gte=start_date, date__lte=timezone.now())

        if not results.exists():
            return data

        for result in results:
            date_js = int(time.mktime(result.date.timetuple())) * 1000
            liters = [date_js, result.liters]
            cubic_meters = [date_js, result.cubic_meters]
            data['liters'].append(liters)
            data['cubic_meters'].append(cubic_meters)

        start_date = current_date - one_hour
        start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
        current_date = timezone.make_aware(current_date, timezone.get_default_timezone())
        total_l = Water.objects.get_total_liters(start_date, current_date)
        total_m3 = Water.objects.get_total_m3(start_date, current_date)
        cost = Water.objects.get_cost(cost_m3, start_date, current_date)

        if (total_l is not None) and (total_m3 is not None) and (cost is not None):
            data['total_l'].append(Water.objects.get_total_liters(start_date, current_date))
            data['total_m3'].append(Water.objects.get_total_m3(start_date, current_date))
            data['cost'].append(Water.objects.get_cost(cost_m3, start_date, current_date))

        return data

