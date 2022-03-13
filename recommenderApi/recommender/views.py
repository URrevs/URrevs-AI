from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    response = {
        'message': 'Hello, world!!'
    }
    return JsonResponse(response)