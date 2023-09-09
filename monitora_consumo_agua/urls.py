from django.urls import path

from .views import *


urlpatterns = [
    path('teste/', Testeview.as_view(), name='teste-view'),
]
