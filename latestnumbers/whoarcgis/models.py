from django.db import models


class Statistic(models.Model):
    country_code = models.CharField(max_length=10)
    country_code_2 = models.CharField(max_length=2, blank=True, null=True)  # Iso - 2
    updated_at = models.DateTimeField()
    new_cases = models.IntegerField(default=0)
    cum_cases = models.IntegerField(default=0)
    new_deaths = models.IntegerField(default=0)
    cum_deaths = models.IntegerField(default=0)
    total_vaccinations = models.IntegerField(default=0)
