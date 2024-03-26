# views.py
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from aviation.models import Flight

class BookingView(APIView):
  permission_classes =[IsAuthenticated]
  def post(self, request, format=None):
    departure_airport = request.data['departure_airport']
    print("departure_airport: ", departure_airport)

    return JsonResponse
      