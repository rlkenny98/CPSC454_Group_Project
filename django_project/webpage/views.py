from django.shortcuts import render
from django.http import HttpResponse
from django_project.custom_storage import MediaStorage
from django.core.files.storage import default_storage
from django_project import settings, encryption
from boto3.session import Session
import boto3

# TO-DO @Maria: Link to any html files here
#EXAMPlE

def home(request):
    return render(request, 'webpage/base.html')

def upload(request):
    enc = encryption
    if request.method == "POST":
        # if the post request has a file under the input name 'document', then save the file.
        request_file = request.FILES['document'] if 'document' in request.FILES else None
        if request_file:
                # save attatched file
                # create a new instance of FileSystemStorage

                """CRITICAL NOTE: we need to manage our KMS permissions... not sure how"""
                # check if customer master key exists for this file 
                cmkID,cmkArn = enc.retrieve_cmk(request_file.name)
                if not cmkID:
                    # create key if CMK does not exist
                    enc.create_cmk(request_file.name)
                    cmkID,cmkArn = enc.retrieve_cmk(request_file.name)

                # not sure if this is right
                enc.create_data_key(cmkID)
                enc.encrypt_file(request_file.name,cmkID)

                media = MediaStorage()
                file = media.save(request_file.name, request_file)
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                file= media.url(file)

    return render(request, 'webpage/upload.html',{'file':'file'})

def about(request):
    return render(request, 'webpage/about.html')

def uploadDownload(request):
    return render(request, 'webpage/uploadDownload.html')

def download(request):
    media = MediaStorage()
    bucket = media.bucket_name

    
    client = boto3.client('s3',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    paginator = client.get_paginator('list_objects_v2')
    result = paginator.paginate(Bucket=bucket)

    location = client.get_bucket_location(Bucket=bucket)['LocationConstraint']

    fileUrl = ''
    contents = {}
    #URLs = []
    for page in result:
        if "Contents" in page:
            for key in page[ "Contents" ]:

                keyString = key[ "Key" ]


                fileUrl = f'https://s3-{location}.s3.amazonaws.com/{bucket}/{keyString}'
                keyString = keyString[6:]
                print("File Name and its URL:", keyString, ", ",fileUrl)
                # print(fileUrl)
                contents[keyString] = fileUrl

    return render(request, 'webpage/download.html',{'bucket':contents})

    """
    fileObjects = media.listdir("")
    fileObjects = fileObjects[1]
    
    for file in  fileObjects:
        print(file)
        fileObject = media.open(file)

    return render(request, 'webpage/download.html',{'filelist':fileObjects})"""