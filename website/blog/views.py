from django.shortcuts import render
from django.http import HttpResponse

def home(reqest):
    return HttpResponse('<h1>Hello world<h1>')

def test(reqest):
    return HttpResponse('<h1>Test page<h1>')
