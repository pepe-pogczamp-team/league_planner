from django.db.models import Case, F, OuterRef, Q, QuerySet, Subquery, Sum, Value, When
from rest_framework import status
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
from league_planner.models.match import Match
from league_planner.models.team import Team
from league_planner.pagination import Pagination
from league_planner.serializers.league import LeagueSerializer
from league_planner.serializers.team import ScoreboardSerializer

if TYPE_CHECKING:
    from typing import Any, Self


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

    def create(self: "Self", request: "Request", *args: "Any", **kwargs: "Any") -> "Response":
        request.data["owner"] = request.user.pk
        return super().create(request, *args, **kwargs)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"(?P<league_id>\w+)/scoreboard",
    )
    def scoreboard(self: "Self", request: "Request", league_id: int) -> "Response":
        scoreboard_queryset = self.scoreboard_queryset(league_id)
        page = self.paginate_queryset(scoreboard_queryset)
        if page is not None:
            data = ScoreboardSerializer(page, many=True).data
            return self.get_paginated_response(data)
        data = ScoreboardSerializer(scoreboard_queryset, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def scoreboard_queryset(self: "Self", league_id: int) -> "QuerySet":
        matches_with_points_qs = self.matches_with_points_queryset(league_id)
        return Team.objects.filter(league_id=league_id).annotate(
            points_as_host=Sum(
                Subquery(
                    matches_with_points_qs.filter(host_id=OuterRef("id")).values("host_points"),
                ),
                default=Value(0),
            ),
            points_as_visitor=Sum(
                Subquery(
                    matches_with_points_qs.filter(visitor_id=OuterRef("id")).values("visitor_points"),
                ),
                default=Value(0),
            ),
            score=(F("points_as_host") + F("points_as_visitor")),
        ).order_by("-score")

    @staticmethod
    def matches_with_points_queryset(league_id: int) -> "QuerySet":
        return Match.objects.filter(league_id=league_id).annotate(
            host_points=Case(
                When(
                    Q(host_score__isnull=True) | Q(visitor_score__isnull=True),
                    then=Value(0),
                ),
                When(host_score__gt=F("visitor_score"), then=Value(3)),
                When(host_score=F("visitor_score"), then=Value(1)),
                default=Value(0),
            ),
            visitor_points=Case(
                When(
                    Q(host_score__isnull=True) | Q(visitor_score__isnull=True),
                    then=Value(0),
                ),
                When(visitor_score__gt=F("host_score"), then=Value(3)),
                When(visitor_score=F("host_score"), then=Value(1)),
                default=Value(0),
            )
        )
