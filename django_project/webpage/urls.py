from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # TO-DO @Maria : Define webpage URLs here
    #EXAMPlE:
        path('', views.home, name='webpage-home'), #sign in page
        path('about/', views.about, name='webpage-about'),
        path('upload_download/', views.uploadDownload, name='webpage-upload-download'),
        path('download/', views.download, name='webpage-download'),
        path('upload/', views.upload, name='webpage-sign-in'),
]

# only in development
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
