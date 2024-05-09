from django.shortcuts import render

# Create your views here.


def index(request):
    time = [f"{i}:00" for i in range(24)]
    return render(request, 'index.html', {'time': time})
