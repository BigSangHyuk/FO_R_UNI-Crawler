from django.urls import path
from Crawler.views import Showdata

urlpatterns = [
    path("", Showdata),
]
