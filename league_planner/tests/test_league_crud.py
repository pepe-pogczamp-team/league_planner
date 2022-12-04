import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from factories import LeagueFactory, MatchFactory, TeamFactory
from league_planner.models.league import League
from league_planner.models.match import Match
from league_planner.models.team import Team

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def create_league_data() -> dict:
    return {
        "name": "NBA",
    }


def test_leagues_list(
    api_client: "APIClient",
    league_factory: "LeagueFactory",
) -> None:
    url = reverse("leagues-list")
    for i in range(10):
        league_factory.create(name=f"league{i}")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["count"] == 10


def test_league_detail(
    api_client: "APIClient",
    league_factory: "LeagueFactory",
) -> None:
    league = league_factory.create(name="NBA")
    url = reverse("leagues-detail", args=[league.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["name"] == league.name
    assert response.data["owner"] == league.owner.pk


def test_league_create(
    api_client: "APIClient",
    test_user: "User",
    create_league_data: dict,
) -> None:
    url = reverse("leagues-list")
    response = api_client.post(url, data=create_league_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED, response
    assert response.data["name"] == create_league_data["name"]
    assert response.data["owner"] == test_user.pk
    league = League.objects.get(name=create_league_data["name"])
    assert league.name == create_league_data["name"]
    assert league.owner == test_user


def test_league_update(
    api_client: "APIClient",
    league_factory: "LeagueFactory",
    create_league_data: dict,
) -> None:
    league = league_factory.create(**create_league_data)
    url = reverse("leagues-detail", args=[league.pk])
    update_data = {"name": "WNBA"}
    response = api_client.patch(url, data=update_data, format="json")
    assert response.status_code == status.HTTP_200_OK, response
    assert response.data["name"] == update_data["name"]
    league.refresh_from_db()
    assert league.name == update_data["name"]


def test_league_destroy(
    api_client: "APIClient",
    league_factory: "LeagueFactory",
    team_factory: "TeamFactory",
    match_factory: "MatchFactory",
) -> None:
    league = league_factory.create()
    team = team_factory.create(league=league)
    match = match_factory.create(league=league, host=team)
    url = reverse("leagues-detail", args=[league.pk])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response
    with pytest.raises(League.DoesNotExist):
        League.objects.get(id=league.pk)
    with pytest.raises(Team.DoesNotExist):
        Team.objects.get(id=team.pk)
    with pytest.raises(Match.DoesNotExist):
        Match.objects.get(id=match.pk)
