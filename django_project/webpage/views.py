from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

# TO-DO @Maria: Link to any html files here
#EXAMPlE

  
def home(request):
    if request.method == "POST":
        # if the post request has a file under the input name 'document', then save the file.
        request_file = request.FILES['document'] if 'document' in request.FILES else None
        if request_file:
                # save attatched file

                # create a new instance of FileSystemStorage
                fs = FileSystemStorage()
                file = fs.save(request_file.name, request_file)
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                fileurl = fs.url(file)

    return render(request, 'webpage/home.html')
def about(request):
    return render(request, 'webpage/about.html')
