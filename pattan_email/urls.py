from django.urls import path
from . import views

app_name = "communications"

urlpatterns = [
    path('event/<int:event_id>', views.index, name='index'),
]
