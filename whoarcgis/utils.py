from datetime import datetime, timedelta

import requests
from django.utils import timezone

from .models import Statistic

now_aware = timezone.now()
feature_server_url = "https://services.arcgis.com/5T5nSi527N4F7luB/arcgis/rest/services/COVID_19_Historic_cases_by_country_pt_v7_view/FeatureServer/0"


def should_not_have_to_update(updated_at):
    diff_more_than_hour = (now_aware - updated_at) < timedelta(hours=1)
    print("Difference is less than an hour: ", diff_more_than_hour)
    return diff_more_than_hour


def less_than_a_day_old(updated_at):
    diff_more_than_day = (now_aware - updated_at) < timedelta(days=1)
    print("Difference is less than a day: ", diff_more_than_day)
    return diff_more_than_day


def retrieve_country_stats_from_arcgis(country_code):
    try:
        stat = Statistic.objects.get(country_code=country_code)
    except Statistic.DoesNotExist:
        stat = None
    if stat and should_not_have_to_update(stat.updated_at):
        return {
            "country_code": stat.country_code,
            "new_cases": stat.new_cases,
            "cum_cases": stat.cum_cases,
            "new_deaths": stat.new_deaths,
            "cum_deaths": stat.cum_deaths,
            "total_vaccinations": stat.total_vaccinations,
        }
    print("retrieving from ArcGIS")
    url = (
        feature_server_url
        + f"/query?where=ISO_3_CODE+%3D+'{country_code}'&returnGeometry=false&outFields=NewCase,CumCase,NewDeath,CumDeath,date_epicrv,ISO_2_CODE&f=json"
    )
    response = requests.get(url).json()
    features = response["features"]
    latest = features.pop()["attributes"]
    yesterday = features.pop()["attributes"] if features.pop() else None
    if latest["NewCase"] == 0 and latest["NewDeath"] == 0:
        if stat and less_than_a_day_old(stat.updated_at):
            return {
                "country_code": stat.country_code,
                "new_cases": stat.new_cases,
                "cum_cases": stat.cum_cases,
                "new_deaths": stat.new_deaths,
                "cum_deaths": stat.cum_deaths,
                "total_vaccinations": stat.total_vaccinations,
            }
        # get vaccinations
        vaccinations = requests.get(
            "https://covid19.who.int/who-data/vaccination-data.json"
        ).json()
        total_vaccinations = 0
        for x in vaccinations["data"]:
            if x["ISO3"] == country_code:
                total_vaccinations = x["TOTAL_VACCINATIONS"]
                break
        if yesterday and yesterday["NewCase"] != 0:
            stat = Statistic.objects.create(
                country_code=country_code,
                country_code_2=yesterday["ISO_2_CODE"],
                updated_at=datetime.fromtimestamp(yesterday["date_epicrv"] / 1000),
                new_cases=yesterday["NewCase"],
                cum_cases=yesterday["CumCase"],
                new_deaths=yesterday["NewDeath"],
                cum_deaths=yesterday["CumDeath"],
                total_vaccinations=total_vaccinations,
            )
        else:
            stat = Statistic.objects.create(
                country_code=country_code,
                country_code_2=latest["ISO_2_CODE"],
                updated_at=datetime.fromtimestamp(latest["date_epicrv"] / 1000),
                new_cases=latest["NewCase"],
                cum_cases=latest["CumCase"],
                new_deaths=latest["NewDeath"],
                cum_deaths=latest["CumDeath"],
                total_vaccinations=total_vaccinations,
            )
        return {
            "country_code": stat.country_code,
            "new_cases": stat.new_cases,
            "cum_cases": stat.cum_cases,
            "new_deaths": stat.new_deaths,
            "cum_deaths": stat.cum_deaths,
            "total_vaccinations": stat.total_vaccinations,
        }


def retrieve_global_stats_from_arcgis():
    try:
        stat = Statistic.objects.get(country_code="Global", cum_cases__gt=0)
    except Statistic.DoesNotExist:
        stat = None
    if stat and should_not_have_to_update(stat.updated_at):
        return {
            "country_code": stat.country_code,
            "new_cases": stat.new_cases,
            "cum_cases": stat.cum_cases,
            "new_deaths": stat.new_deaths,
            "cum_deaths": stat.cum_deaths,
        }
    print("retrieving from ArcGIS")
    date = datetime.today().strftime("%m/%d/%Y")
    url = (
        feature_server_url
        + f"/query?where=date_epicrv+%3D+'{date}'&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=NewCase%2CNewDeath%2Cdate_epicrv%2CADM0_name&returnGeometry=true&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=%5B%7B%22statisticType%22%3A+%22sum%22%2C%22onStatisticField%22%3A+%22NewCase%22%2C%22outStatisticFieldName%22%3A+%22NewCase%22%7D%2C%0D%0A%7B%22statisticType%22%3A+%22sum%22%2C%22onStatisticField%22%3A+%22CumCase%22%2C%22outStatisticFieldName%22%3A+%22CumCase%22%7D%2C%0D%0A%7B%22statisticType%22%3A+%22sum%22%2C%22onStatisticField%22%3A+%22CumDeath%22%2C%22outStatisticFieldName%22%3A+%22CumDeath%22%7D%2C%7B%22statisticType%22%3A+%22sum%22%2C%22onStatisticField%22%3A+%22NewDeath%22%2C%22outStatisticFieldName%22%3A+%22NewDeath%22%7D%0D%0A%5D&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token="
    )
    response = requests.get(url).json()
    features = response["features"]
    latest = features.pop()["attributes"]
    if (
        stat
        and latest["NewCase"] == 0
        and (latest["NewDeath"] is None or latest["CumCase"] < stat.cum_cases)
    ):
        return {
            "country_code": stat.country_code,
            "new_cases": stat.new_cases,
            "cum_cases": stat.cum_cases,
            "new_deaths": stat.new_deaths,
            "cum_deaths": stat.cum_deaths,
        }
    stat = Statistic.objects.create(
        country_code="Global",
        updated_at=datetime.now(),
        new_cases=latest["NewCase"],
        cum_cases=latest["CumCase"],
        new_deaths=latest["NewDeath"],
        cum_deaths=latest["CumDeath"],
    )
    return {
        "country_code": stat.country_code,
        "new_cases": stat.new_cases,
        "cum_cases": stat.cum_cases,
        "new_deaths": stat.new_deaths,
        "cum_deaths": stat.cum_deaths,
    }


def retrieve_contact_language(msisdn, turn_token, turn_url):
    print("getting contact from turn")
    headers = {
        "Accept": "application/vnd.v1+json",
        "Authorization": f"Bearer {turn_token}",
    }
    response = requests.get(f"{turn_url}/v1/contacts/{msisdn}/profile", headers=headers)
    return response.json()["data"]["fields"]["language"]


def retrieve_latest_news():
    date = datetime.today().strftime("%m/%d/%Y")
    rss_feed_url = f"https://www.who.int/rss-feeds/news-english.xml?req_time={date}"
    response = requests.get(rss_feed_url)
    return response.content
