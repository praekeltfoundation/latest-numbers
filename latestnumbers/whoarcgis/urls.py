from django.contrib import admin
from django.urls import path, include
from .views import get_stats_country, get_stats_global, get_latest_news


urlpatterns = [
    path('stats/country', get_stats_country),
    path('stats/global', get_stats_global),
    path('news', get_latest_news),
]
