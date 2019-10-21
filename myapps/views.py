from django.shortcuts import render

def myapps(request):
    return render(request, 'myapps/index.html')
