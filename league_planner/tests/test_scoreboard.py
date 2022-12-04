import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from factories import LeagueFactory, TeamFactory, MatchFactory

pytestmark = [pytest.mark.django_db]


def test_scoreboard(
    api_client: "APIClient",
    league_factory: "LeagueFactory",
    team_factory: "TeamFactory",
    match_factory: "MatchFactory",
) -> None:
    league = league_factory.create()
    url = reverse("leagues-detail", args=[league.pk])
    team1 = team_factory.create(
        name="Polska",
        league=league,
    )
    team2 = team_factory.create(
        name="Argentyna",
        league=league,
    )
    match_factory.create(
        league=league,
        host=team1,
        visitor=team2,
        host_score=0,
        visitor_score=2,
    )
    response = api_client.get(f"{url}scoreboard/")
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["count"] == 2
    teams = response.data["results"]
    assert teams[0]["name"] == "Argentyna"
    assert teams[0]["score"] == 3
    assert teams[1]["name"] == "Polska"
    assert teams[1]["score"] == 0
