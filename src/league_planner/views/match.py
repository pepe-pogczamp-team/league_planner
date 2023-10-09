import datetime
from typing import TYPE_CHECKING

from rest_framework import viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated

from league_planner import settings
from league_planner.filters import FilterByLeague
from league_planner.integrations.weather import WeatherAPIClient
from league_planner.models.match import Match
from league_planner.models.team import Team
from league_planner.pagination import Pagination
from league_planner.permissions import IsLeagueResourceOwner
from league_planner.serializers.match import MatchSerializer

if TYPE_CHECKING:
    from typing import Any
    from rest_framework.request import Request
    from rest_framework.response import Response


class MatchViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    permission_classes = (IsAuthenticated, IsLeagueResourceOwner)
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    pagination_class = Pagination
    filterset_class = FilterByLeague

    def create(self, request: "Request", *args: "Any", **kwargs: "Any") -> "Response":
        response = super().create(request, *args, **kwargs)

        host_city = Team.objects.get(id=request.data.get("host")).city
        match_datetime = datetime.datetime.strptime(
            request.data.get("datetime"),
            settings.FE_DATETIME_FORMAT,
        )

        if host_city and match_datetime:
            weather_api_client = WeatherAPIClient()
            is_weather_good = weather_api_client.check_if_weather_good(
                host_city,
                match_datetime,
            )
        else:
            is_weather_good = True

        response.data["is_weather_good"] = is_weather_good
        return response
