from django.urls import path
from . import views

urlpatterns = [
    path('event/<id>', views.Event.as_view(), name='test'),
    path('t1/<id>', views.t1)
]