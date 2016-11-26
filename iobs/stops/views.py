from django.shortcuts import render
from django.http import HttpResponse
from .models import BusStop, SensorData


def start_view(request):
    # get the buss stop associated with this session
    if 'stop_id' not in request.session:
        count = BusStop.objects.filter().count()
        stop = BusStop.objects.create(name="Bus stop {}".format(count),
                              lat=0,
                              lng=0)
        stop.save()
        request.session['stop_id'] = stop.id
    else:
        stop = BusStop.objects.get(id=request.session['stop_id'])

    return render(request, 'stop/game.html', {'stop': stop})



def sensor_test(request):
    busid = BusStop.objects.get(id=request.GET['busid'])
    stype = request.GET['stype']
    svalue = request.GET['svalue']
    rawvalue = request.GET['rawvalue']

    data = dict(request.GET.items())
    sdata = SensorData(r_type=stype, value_raw=rawvalue, value_converted=svalue, bus_stop=busid)
    sdata.save()

    return HttpResponse("You sent {}".format(data))



