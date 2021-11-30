from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django_project.custom_storage import MediaStorage
#from django.core.files.storage import default_storage
from users.models import Profile
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage
import hashlib
# TO-DO @Maria: Link to any html files here
#EXAMPlE

token = ''
token_size = 0

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
                filename = f'{token.hexdigest()}_{request_file.name}'
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
    token = hashlib.md5(str.encode(request.user.username))
    token_size = token.__sizeof__()
    token_str = token.hexdigest()
    dict = {}

    filelist = media.listdir("")
    filelist = filelist[1]
    #print(filelist[1])
    #Size of token value we have to compare to
    print(token_size)
    print(f'Files for {request.user.username}:')
    for file in filelist:
        #Compare the first n characters of file name with the hashed token string value
        #print(file[:token_size])
        #print(token_str)
        if file[:token_size] == token_str:
            # Removing token value and '+' character from name
            cleaned_name = file[token_size+1:]
            #print(cleaned_name)
            dict[cleaned_name] = file
            #dictList.append(dict)

    return render(request, 'webpage/download.html',{'dictList':dict})