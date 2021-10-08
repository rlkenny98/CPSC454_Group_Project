from django.urls import path
from . import views

urlpatterns = [
    # TO-DO @Maria : Define webpage URLs here
    #EXAMPlE:
        path('', views.home, name='webpage-home'),
        path('about/', views.about, name='webpage-about'),

]