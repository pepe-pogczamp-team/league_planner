import pytest
from rest_framework.test import APIRequestFactory

from league_planner.views.league import LeagueViewSet

factory = APIRequestFactory()


@pytest.mark.django_db
def test_league_list():
    request = factory.get("/leagues/")
    response = LeagueViewSet.as_view(request)
    assert response
