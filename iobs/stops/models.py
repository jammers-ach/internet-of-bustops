from django.db import models

SENSOR_TYPES = (
    ('humid','Humidity'),
    ('temp','Temperature'),
)

class BusStop(models.Model):
    name = models.CharField(max_length=40)
    lat = models.FloatField()
    lng = models.FloatField()
    has_someone = models.BooleanField(default=False)


class SensorData(models.Model):
    timestamp = models.DateTimeField()
    r_type = models.CharField(max_length=20,choices=SENSOR_TYPES)
    value_raw = models.IntegerField()
    value_converted = models.FloatField()
    bus_stop = models.ForeignKey('BusStop')
