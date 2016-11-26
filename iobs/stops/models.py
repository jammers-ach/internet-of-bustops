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

    def __str__(self):
        return '{}'.format(self.name)


class SensorData(models.Model):
    timestamp = models.DateTimeField()
    r_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    value_raw = models.IntegerField()
    value_converted = models.FloatField()
    bus_stop = models.ForeignKey('BusStop')


class Game(models.Model):
    in_progress = models.BooleanField(default=False)
    turn = models.ForeignKey('Player', related_name='current_turn')


class Player(models.Model):
    bus_stop = models.ForeignKey('BusStop')
    game = models.ForeignKey('Game')
    score = models.IntegerField(default=0)
    playing = models.BooleanField(default=True)

class Node(models.Model):
    NODE_POS = ((0, 'up'),
                (1, 'left'))
    x = models.IntegerField()
    y = models.IntegerField()
    pos = models.IntegerField(choices=NODE_POS)

