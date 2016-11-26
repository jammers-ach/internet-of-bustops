from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import BusStop, Game, Node, Player, Box
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

    updated_players = list(players)
    players = players.update(playing=False)

    for player in updated_players:
        if player.current_turn.exists():
            game = player.current_turn.get()
            game.next_turn()
            print('Active player left')


    return HttpResponse("You've left the current game")

def sensor_test(request):
    data = dict(request.GET.items())
    return HttpResponse("You sent {}".format(data))

def game_edge(request, game_id):
    game, _ = Game.objects.get_or_create(id=game_id)

    # TODO check that a node doesn't exist first
    node, created = Node.objects.get_or_create(pos=request.GET['dir'],
                x=request.GET['row'],
                y=request.GET['col'],
                game=game)

    node.moved_id = game.node_set.count() - 1
    node.save()

    return JsonResponse({'ok':created})

def game_cell(request, game_id):
    game, _ = Game.objects.get_or_create(id=game_id)

    # TODO check that a node doesn't exist first
    node, created = Box.objects.get_or_create(
                x=request.GET['row'],
                y=request.GET['col'],
                owner=Player.objects.get(game=game, player_id=request.GET['player']),
                game=game)

    node.save()

    return JsonResponse({'ok':created})

def game_poll(request, game_id):
    after = request.GET.get('after', 0)
    stop = session_stop(request)
    game, _ = Game.objects.get_or_create(id=game_id)

    try:
        player= Player.objects.get(bus_stop=stop, game=game, playing=True)
    except Exception:
        print("Something went wrong")
        return JsonResponse({'ok':False})



    game_dict = game.game_data_json(after=after)
    game_dict['player_id'] = player.player_id

    return JsonResponse({'game_data': game_dict})

def end_turn(request, game_id):
    stop = session_stop(request)
    game, _ = Game.objects.get_or_create(id=game_id)
    player, created = Player.objects.get_or_create(bus_stop=stop, game=game, playing=True)

    game.next_turn()

    return JsonResponse({'ok':not created})
