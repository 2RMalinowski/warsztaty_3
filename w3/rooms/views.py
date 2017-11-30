from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def show_number(request, number):
    html = """ <html><body><p></p></body></html>"""
    answer = html % number
    return HttpResponse(answer)
