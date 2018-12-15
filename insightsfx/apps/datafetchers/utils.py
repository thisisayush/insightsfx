import requests
import dateparser
from django.conf import settings
from psycopg2 import IntegrityError

from apps.pollutionmodels.models import PollutionData, Station

class Extractor(object):

    api_url = ""
    api_params = {}
    source = ""
    source_type = ""

    POST = "post"
    GET = "get"

    def __init__(self):
        pass 

    def send_request(self, method):
        if method == self.GET:
            return requests.get(self.api_url, params = self.api_params)
        if method == self.POST:
            return requests.post(self.api_url, data  = self.api_params)

    def process(self):
        pass

    def store(self, station, source_time, pm_25 = None, pm_10 = None):
        try:
            try:
                p = PollutionData.objects.get(source=self.source, station=station, source_time=source_time)
                if not p.pm25:
                    p.pm25 = pm_25
                if not p.pm10:
                    p.pm10 = pm_10
                p.save()
                print("Updated PM2.5=%s PM10=%s for station %s at %s" %(p.pm25, p.pm10, station, source_time))
            except PollutionData.DoesNotExist:
                p = PollutionData.objects.create(
                    source = self.source,
                    source_type = self.source_type,
                    pm25 = pm_25,
                    pm10 = pm_10,
                    station = station,
                    source_time = source_time
                ) 
                print("Added PM2.5=%s PM10=%s for station %s at %s" %(p.pm25, p.pm10, station, source_time))
            return p
        except IntegrityError:
            return None

class GovernmentExtractor(Extractor):
    
    def __init__(self):
        super().__init__()
        self.api_url = "https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"
        self.api_params = {
            "api-key": settings.DATA_GOV_API_KEY,
            "format": "json",
            "offset": "0",
            "limit": "1000"
        }
        self.source = "data.gov.in"
        self.source_type = PollutionData.GOVERNMENT
    
    def process(self):
        r = self.send_request(self.GET)
        data = r.json()

        for x in data['records']:
            if x['city'].lower() != 'delhi':
                continue
            if x['pollutant_avg'] == "NA":
                continue
            if x['pollutant_id'] != "PM2.5" and x['pollutant_id'] != "PM10":
                continue
            
            station = ' '.join(x['station'].split(",")[:-1])
            try:
                s = Station.objects.get(location = station)
            except Station.DoesNotExist:
                s = Station.objects.create(location = station)

            pm25, pm10 = None, None

            if x['pollutant_id'] == "PM2.5":
                pm25 = x['pollutant_avg']
            if x['pollutant_id'] == "PM10":
                pm10 = x['pollutant_avg']

            data_time = dateparser.parse(x['last_update'])

            self.store(s, data_time, pm25, pm10)