from django.http import HttpResponse
from django.shortcuts import render

def webpage1(request):
    return render(request,"page1.html")

def webpage2(request):
    results=request.GET['fruits']
    return render(request,"page2.html",{'fruits':results})