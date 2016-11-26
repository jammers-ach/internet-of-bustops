from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import BusStop, Game, Node, Player
import json


def session_stop(request):
    if 'stop_id' not in request.session:

        count = BusStop.objects.filter().count()
        stop = BusStop.objects.create(name="Bus stop {}".format(count),
                              lat=0,
                              lng=0)
        stop.save()
        request.session['stop_id'] = stop.id
    else:
        stop = BusStop.objects.get(id=request.session['stop_id'])

    return stop


def start_view(request):
    # get the buss stop associated with this session
    stop = session_stop(request)

    game, _ = Game.objects.get_or_create(id=1)
    player, created = Player.objects.get_or_create(bus_stop=stop, game=game, playing=True)

    if created:
        player.player_id = game.player_set.count() - 1
        player.save()

    game_dict = game.game_data_json()
    game_dict['player_id'] = player.player_id
    game_dict['current_player'] = game_dict['players'][0]

    return render(request, 'stop/game.html', {'stop': stop, 'game': json.dumps(game_dict)})


def leave(request):
    stop = session_stop(request)
    players = Player.objects.filter(bus_stop=stop)

    players.update(playing=False)

    return HttpResponse("You've left the current game")

def sensor_test(request):
    data = dict(request.GET.items())
    return HttpResponse("You sent {}".format(data))

def game(request, game_id):
    game, _ = Game.objects.get_or_create(id=game_id)

    # TODO check that a node doesn't exist first
    node, created = Node.objects.get_or_create(pos=request.GET['dir'],
                x=request.GET['row'],
                y=request.GET['col'],
                game=game)

    node.moved_id = game.node_set.count() - 1
    node.save()

    return JsonResponse({'ok':created})


def game_poll(request, game_id):
    after = request.GET.get('after', 0)
    stop = session_stop(request)
    game, _ = Game.objects.get_or_create(id=game_id)

    player, created = Player.objects.get_or_create(bus_stop=stop, game=game, playing=False)

    if created:
        player.player_id = game.player_set.count() - 1
        player.save()

    game_dict = game.game_data_json(after=after)
    game_dict['player_id'] = player.player_id

    return JsonResponse({'game_data': game_dict})


