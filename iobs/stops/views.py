from django.shortcuts import render
from django.http import HttpResponse
from .models import BusStop

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


    return HttpResponse('You are stop: {}'.format(stop))

