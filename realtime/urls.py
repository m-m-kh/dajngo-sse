from django.urls import path
from . import views

urlpatterns = [
    path('event/', views.Event.as_view(), name='test'),
    path('t1/', views.t1)
]