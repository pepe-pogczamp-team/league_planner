from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from typing import TYPE_CHECKING
from league_planner.models.league import League
from league_planner.pagination import Pagination
from league_planner.serializers.league import LeagueSerializer

if TYPE_CHECKING:
    from typing import Any


class LeagueViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    pagination_class = Pagination

    def create(self, request: "Request", *args: "Any", **kwargs: "Any") -> "Response":
        request.data["owner"] = request.user.pk
        return super().create(request, *args, **kwargs)

    @action(
        methods=["get"],
        detail=False,
        url_path="scoreboard",
    )
    def scoreboard(self, request: "Request") -> "Response":
        return Response()
