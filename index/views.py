from django.shortcuts import render

def index(request, template):
    '''Index'''
    return render(request, template)