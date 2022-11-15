from django.db import models


class Match(models.Model):
    league = models.ForeignKey(
        "league_planner.League",
        on_delete=models.CASCADE,
        verbose_name="Match belong to that League",
    )
    host = models.ForeignKey(
        "league_planner.Team",
        on_delete=models.SET_NULL,
        verbose_name="Host Team",
        related_name="hosts",
        null=True,
    )
    visitor = models.ForeignKey(
        "league_planner.Team",
        on_delete=models.SET_NULL,
        verbose_name="Visitor Team",
        related_name="visitors",
        null=True,
    )
    host_score = models.IntegerField(
        verbose_name="Score of host Team",
        null=True,
    )
    visitor_score = models.IntegerField(
        verbose_name="Score of visitor Team",
        null=True,
    )
    address = models.CharField(
        max_length=100,
        verbose_name="Place where match is played",
        null=True,
    )
    datetime = models.DateTimeField(
        verbose_name="Time when match is played",
        null=True,
    )
