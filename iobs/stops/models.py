from django.db import models
from django.utils import timezone

SENSOR_TYPES = (
    ('humid','Humidity'),
    ('temp','Temperature'),
)


BUS_STOP_NAMES = [
    'Kruunuvuorenkatu 15',
    'Aleksanterinkatu 13',
    'Kruunuvuorenkatu 6',
    'Kaivokatu',
    'Norrtäljentie 1',
    'Laituri 13'
]

class BusStop(models.Model):
    name = models.CharField(max_length=40)
    lat = models.FloatField()
    lng = models.FloatField()
    has_someone = models.BooleanField(default=False)

    def activate(self, active):
        self.has_someone = active
        self.save()

        if active:
            self.join()
        else:
            self.leave()

    def __str__(self):
        return '{}'.format(self.name)

    def leave(self):

        players = Player.objects.filter(bus_stop=self)

        updated_players = list(players)
        players = players.update(playing=False)

        for player in updated_players:
            if player.current_turn.exists():
                game = player.current_turn.get()
                game.next_turn()
                print('Active player left')

    def join(self):
        players = Player.objects.filter(bus_stop=self)
        players.update(playing=True)





class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    r_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    value_raw = models.IntegerField()
    value_converted = models.FloatField()
    bus_stop = models.ForeignKey('BusStop')

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.timestamp, self.r_type, self.value_raw, self.bus_stop)


class Game(models.Model):
    DEFAULT_WIDTH = 4
    DEFAULT_HEIGHT = 4

    # number o fminutes of inactivity
    timeout = 10
    in_progress = models.BooleanField(default=True)
    turn = models.ForeignKey('Player', related_name='current_turn', null=True ,blank=True)

    def __str__(self):
        return "Game {}".format(self.id)

    def game_data_json(self, after=0):
        if self.turn is None and self.active_players.count() > 0:
            self.turn = self.active_players[0]
            self.save()

        if self.turn and not self.turn.playing:
            self.next_turn()

        return {
            'width': self.DEFAULT_WIDTH,
            'height': self.DEFAULT_HEIGHT,
            'nodes': self.node_data(after=after),
            'game_id': self.id,
            'players': [p.player_id for p in self.active_players],
            'score': self.score_data(),
            'current_player': self.turn.player_id if self.turn else -1,
            'stop_names': { p.player_id:p.bus_stop.name for p in self.player_set.all()},
            'over': self.over
        }

    @property
    def over(self):
        return self.box_set.count() == (self.DEFAULT_WIDTH-1) * (self.DEFAULT_HEIGHT-1)

    @property
    def active_players(self):
        return self.player_set.filter(playing=True).order_by('id')

    def node_data(self, after=0):
        return [n.json() for n in self.node_set.filter(move_id__gte=after).order_by('move_id') ]

    def score_data(self):
        data = {}

        for b in self.box_set.all():
            data.setdefault(b.x, {})[b.y] = b.owner.player_id
        return data

    def next_turn(self):
        try:
            index = list(self.active_players).index(self.turn)
            index = (index+1) % self.active_players.count()
        except ValueError:
            index = 0

        try:
            self.turn = self.active_players[index]
            self.save()
        except IndexError:
            self.in_progress = False

    def kick_out(self):
        for player in self.active_players:
            timeout = timezone.now() - player.last_checkin
            if timeout.total_seconds() > self.timeout:
                player.playing = False
                player.save()


class Player(models.Model):
    bus_stop = models.ForeignKey('BusStop')
    game = models.ForeignKey('Game')
    score = models.IntegerField(default=0)
    playing = models.BooleanField(default=True)
    player_id = models.IntegerField(default=0)
    last_checkin = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Player {}".format(self.id)

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

class Box(models.Model):
    game = models.ForeignKey('Game')
    x = models.IntegerField()
    y = models.IntegerField()
    owner = models.ForeignKey('Player')

