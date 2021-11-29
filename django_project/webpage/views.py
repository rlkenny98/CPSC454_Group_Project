from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django_project.custom_storage import MediaStorage
from django.core.files.storage import default_storage
from users.models import Profile
from django.contrib.auth.models import User

import hashlib
# TO-DO @Maria: Link to any html files here
#EXAMPlE

@login_required
def home(request):
    return render(request, 'webpage/base.html')

@login_required
def upload(request):
    if request.method == "POST":
        # if the post request has a file under the input name 'document', then save the file.
        request_file = request.FILES['document'] if 'document' in request.FILES else None
        print(request.user.username)
        token = hashlib.md5(str.encode(request.user.username))
        print(token.hexdigest())
        if request_file:
                # save attatched file
                # create a new instance of FileSystemStorage
                media = MediaStorage()
                filename = f'{token.hexdigest()}+{request_file.name}'
                print(filename)
                file = media.save(filename, request_file)
                # file = media.upload_file(request_file.name, request_file, ExtraArgs={"Metadata": {"x-amz-meta-filetoken": token}})
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                fileurl = media.url(file)
                
    return render(request, 'webpage/upload.html',{'file':'file'})

@login_required
def about(request):
    return render(request, 'webpage/about.html')

#@login_required
def uploadDownload(request):
    return render(request, 'webpage/uploadDownload.html')

@login_required
def download(request):
    media = MediaStorage()

    filelist = media.listdir("")

    filelist = filelist[1] 
     
    return render(request, 'webpage/download.html',{'filelist':filelist})