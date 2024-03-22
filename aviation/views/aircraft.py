from django.http import HttpResponse, HttpRequest
from django.template import loader
from ..models import Aircraft

def aircraft_view(request: HttpRequest):

    template = loader.get_template("aircraft.html")
    aircrafts = Aircraft.objects.all().values()

    context = {"data": aircrafts}
    return HttpResponse(template.render(context, request), content_type="text/html")
