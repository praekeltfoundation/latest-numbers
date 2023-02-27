from django.http import HttpResponse, JsonResponse

from .utils import (  # isort:skip
    retrieve_country_stats_from_arcgis,
    retrieve_global_stats_from_arcgis,
    retrieve_latest_news,
)


def get_stats_country(request):
    country_code = request.GET.get("country_code")
    statistic = retrieve_country_stats_from_arcgis(country_code)
    return JsonResponse(statistic)


def get_stats_global(request):
    stats = retrieve_global_stats_from_arcgis()
    return JsonResponse(stats)


def get_latest_news(request):
    news = retrieve_latest_news()
    return HttpResponse(news)
