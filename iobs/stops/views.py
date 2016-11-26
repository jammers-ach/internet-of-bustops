from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import BusStop, Game, Node, Player, Box, BUS_STOP_NAMES, SensorData
import json


def session_stop(request):
    if 'stop_id' not in request.session:

        count = BusStop.objects.filter().count()
        stop = BusStop.objects.create(name="Bus stop {}".format(count),
                              lat=0,
                              lng=0)

        stop.save()
        stop.name = BUS_STOP_NAMES[stop.id % len(BUS_STOP_NAMES)]
        stop.save()
        request.session['stop_id'] = stop.id
    else:
        stop = BusStop.objects.get(id=request.session['stop_id'])

    return stop

def activate_view(request):
    stop = session_stop(request)
    stop.activate(not stop.has_someone)

    if not stop.has_someone:
        leave(request)
    else:
        join(request)

    return HttpResponse('Stop {} is {}'.format(
        stop.name,
        'now active' if stop.has_someone else 'not active anymore'
    ))


def start_view(request):
    # get the buss stop associated with this session
    stop = session_stop(request)

    game, _ = Game.objects.get_or_create(id=1)


    player, created = Player.objects.get_or_create(bus_stop=stop, game=game)

    if not player.playing:
        player.playing = True
        player.save()

    if created:
        player.player_id = game.player_set.count() - 1
        player.save()

    game_dict = game.game_data_json()
    game_dict['player_id'] = player.player_id
    game_dict['current_player'] = game_dict['players'][0]
    game_dict['active'] = stop.has_someone

    return render(request, 'stop/game.html', {'stop': stop, 'game': json.dumps(game_dict)})

def join(request):
    stop = session_stop(request)
    stop.join()
    return HttpResponse("You're joining the games")


def leave(request):
    stop = session_stop(request)
    stop.leave()
    return HttpResponse("You've left the current game")

def sensor_test(request):
    stop = BusStop.objects.get(id=request.GET['busid'])
    stype = request.GET['stype']
    svalue = request.GET['svalue']
    rawvalue = request.GET['rawvalue']
    data = dict(request.GET.items())
    sdata = SensorData(r_type=stype, value_raw=rawvalue, value_converted=svalue, bus_stop=stop)
    sdata.save()

    extra =''
    if stype == 'pir':
        active = rawvalue == '1'
        stop.activate(active)
        if active:
            stop.join()
            extra = "Bus stop joined a game"
        else:
            stop.leave()
            extra = "Bus stop lefta game"


    return HttpResponse("You sent {}<br/>{}".format(data, extra))


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

    game_dict = game.game_data_json(after=after)
    try:
        player = Player.objects.get(bus_stop=stop, game=game, playing=True)
        game_dict['player_id'] = player.player_id
    except Exception:
        pass

    game_dict['active'] = stop.has_someone

    return JsonResponse({'game_data': game_dict})

def end_turn(request, game_id):
    game, _ = Game.objects.get_or_create(id=game_id)

    try:
        game.next_turn()
        return JsonResponse({'ok':True})
    except Exception:
        return JsonResponse({'ok':False})



