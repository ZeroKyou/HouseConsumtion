from django.db.models import Manager, Avg, Sum


class ElectricityManager(Manager):

    def save_reading(self, irms):
        irms = round(irms/100.0, 2)
        self.create(current=irms)

    def get_avg_current(self, start_date, end_date):
        avg_current = self.filter(date__gte=start_date, date__lt=end_date).aggregate(Avg('current'))
        if avg_current['current__avg'] is None:
            return None
        return round(avg_current['current__avg'], 2)

    def get_avg_voltage(self, start_date, end_date):
        avg_voltage = self.filter(date__gte=start_date, date__lt=end_date).aggregate(Avg('voltage'))
        return avg_voltage['voltage__avg']

    def get_avg_power(self, start_date, end_date):
        avg_power = 0
        results = self.filter(date__gte=start_date, date__lt=end_date)

        if not results.exists():
            return None

        for result in results:
            avg_power += result.power

        return round(avg_power/len(results), 2)

    def get_cost(self, cost_kw_h, start_date, end_date):
        avg_power = self.get_avg_power(start_date, end_date)
        results = self.filter(date__gte=start_date, date__lt=end_date)
        if not results.exists():
            return None
        date_first_reading = results.first().date
        date_last_reading = results.last().date
        hours = date_last_reading - date_first_reading
        hours = max(1, float(hours.total_seconds()) / 3600)
        avg_power_kw = float(avg_power)/1000
        cost = hours * avg_power_kw * cost_kw_h
        return round(cost, 2)


class WaterManager(Manager):

    def save_reading(self, water_meter_cycles):
        liters = float(water_meter_cycles*0.5)
        self.create(liters=liters)

    def get_total_liters(self, start_date, end_date):
        total_liters = self.filter(date__gte=start_date, date__lt=end_date).aggregate(Sum('liters'))
        return total_liters['liters__sum']

    def get_total_m3(self, start_date, end_date):
        total_m3 = 0
        results = self.filter(date__gte=start_date, date__lt=end_date)

        if not results.exists():
            return None

        for result in results:
            total_m3 += result.cubic_meters

        return total_m3

    def get_cost(self, cost_m3, start_date, end_date):
        total_m3 = self.get_total_m3(start_date, end_date)
        if total_m3 is None:
            return None
        return round(total_m3 * cost_m3, 2)


class SettingsManager(Manager):

    def send_email(self, values):
        '''
        Returns a list of user emails whose Settings' "send_email" attribute is True
        and "power_warning" and "liters_warning" are less than the ones provided in "values"
        :param values: power and liters of water read
        :return: List of emails
        '''
        emails = []
        power = values['power']
        water_liters = values['water_liters']
        users_to_send_email = self.filter(send_email=True)
        users_settings = users_to_send_email.filter(
            power_warning__lt=power) | users_to_send_email.filter(liters_warning__lt=water_liters)
        if users_settings.exists():
            for user_settings in users_settings:
                if user_settings.ok_to_send():
                    emails.append(user_settings.user.email)
        return emails
