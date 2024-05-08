from django.urls import path
from . import views

urlpatterns = [
    path('event/', views.sse, name='test'),
    path('t1/', views.t1, )
]