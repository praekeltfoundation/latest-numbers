from django.urls import path

from .views import get_latest_news, get_stats_country, get_stats_global

urlpatterns = [
    path("stats/country", get_stats_country),
    path("stats/global", get_stats_global),
    path("news", get_latest_news),
]
