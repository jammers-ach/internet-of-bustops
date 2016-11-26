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
    DEFAULT_WIDTH = 5
    DEFAULT_HEIGHT = 5
    in_progress = models.BooleanField(default=False)
    # turn = models.ForeignKey('Player', related_name='current_turn')

    def game_data_json(self, after=0):
        return {
            'width': self.DEFAULT_WIDTH,
            'height': self.DEFAULT_HEIGHT,
            'nodes': self.node_data(after=after),
            'game_id': self.id,
            'players': [p.player_id for p in self.player_set.filter(playing=True).order_by('id')]

        }

    def node_data(self, after=0):
        return [n.json() for n in self.node_set.filter(move_id__gte=after).order_by('move_id') ]

class Player(models.Model):
    bus_stop = models.ForeignKey('BusStop')
    game = models.ForeignKey('Game')
    score = models.IntegerField(default=0)
    playing = models.BooleanField(default=True)
    player_id = models.IntegerField(default=0)

class Node(models.Model):
    NODE_POS = ((0, 'up'),
                (1, 'left'))
    x = models.IntegerField()
    y = models.IntegerField()
    pos = models.IntegerField(choices=NODE_POS)
    game = models.ForeignKey('Game')
    move_id = models.IntegerField(default=0)

    def json(self):
        return [self.x, self.y, self.pos]

    def __str__(self):
        return "Game {} move {}".format(self.game.id, self.move_id)
