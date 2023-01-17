from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def api_home(requests, *args, **kwargs):
    return JsonResponse({"message": "Hi there, this is your Django API response."})