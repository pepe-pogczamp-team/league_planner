from datetime import datetime

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
    team3 = team_factory.create(
        name="Meksyk",
        league=league,
    )
    match_factory.create(
        league=league,
        host=team1,
        visitor=team2,
        host_score=0,
        visitor_score=2,
        datetime=datetime.now(),
    )
    match_factory.create(
        league=league,
        host=team1,
        visitor=team3,
        host_score=0,
        visitor_score=0,
        datetime=datetime.now(),
    )
    match_factory.create(
        league=league,
        host=team3,
        visitor=team2,
        host_score=0,
        visitor_score=2,
        datetime=datetime.now(),
    )
    match_factory.create(
        league=league,
        host=None,
        visitor=None,
        datetime=datetime.now(),
    )
    response = api_client.get(f"{url}scoreboard/")
    assert response.status_code == status.HTTP_200_OK, response
    assert len(response.data) == 3
    teams = response.data
    assert teams[0]["name"] == "Argentyna"
    assert teams[1]["name"] == "Meksyk"
    assert teams[2]["name"] == "Polska"
    assert teams[0]["score"] == 6
    assert teams[1]["score"] == 1
    assert teams[2]["score"] == 1
