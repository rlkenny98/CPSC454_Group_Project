from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # TO-DO @Maria : Define webpage URLs here
    #EXAMPlE:
        path('', views.home, name='webpage-home'),
        path('about/', views.about, name='webpage-about'),

]

# only in development
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
