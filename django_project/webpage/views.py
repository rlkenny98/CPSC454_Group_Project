from django.shortcuts import render


# TO-DO @Maria: Link to any html files here
#EXAMPlE

  
def home(request):
    return render(request, 'webpage/home.html')


def about(request):
    return render(request, 'webpage/about.html')