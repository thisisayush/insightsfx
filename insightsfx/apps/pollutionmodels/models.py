from django.db import models
import aqi

class Station(models.Model):
    location = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.location

class PollutionData(models.Model):

    GOVERNMENT = "government"
    PRIVATE = "private"
    
    source_type_choices = (
        (GOVERNMENT, "Government"),
        (PRIVATE, "Private")
    )

    source = models.CharField(max_length=255)
    source_type = models.CharField(choices=source_type_choices, max_length=15)

    pm25 = models.FloatField(null=True)
    pm10 = models.FloatField(null=True)

    source_time = models.DateTimeField()

    created_on = models.DateTimeField(auto_now_add=True)
    
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    def __str__(self):
        return "2.5: %s 10: %s Station - %s" % (self.pm25, self.pm10, self.station.location)
    
    class Meta:
        unique_together = (('source', 'station', 'source_time'))