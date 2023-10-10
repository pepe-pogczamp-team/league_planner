from collections import OrderedDict
from typing import Any

from django.db.models import Case, F, QuerySet, Value, When
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from league_planner.models.league import League
from league_planner.models.match import Match
from league_planner.models.team import Team
from league_planner.pagination import Pagination
from league_planner.permissions import IsLeagueOwner
from league_planner.serializers.league import LeagueSerializer
from league_planner.serializers.team import ScoreboardSerializer


class LeagueViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    permission_classes = (IsAuthenticated, IsLeagueOwner)
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    pagination_class = Pagination
    POINTS_PER_WIN = 3
    POINTS_PER_DRAW = 1
    POINTS_PER_LOSE = 0

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request.data["owner"] = request.user.pk
        return super().create(request, *args, **kwargs)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"(?P<league_id>\w+)/scoreboard",
    )
    def scoreboard(self, request: Request, league_id: int) -> Response:
        teams_queryset = self.teams_queryset(league_id)
        teams_to_points_map = {team.id: [0, 0] for team in teams_queryset}
        matches_with_points_qs = self.matches_with_points_queryset(league_id)
        for match in matches_with_points_qs:
            if match.host_id is not None:
                teams_to_points_map[match.host_id][0] += match.host_points
            if match.visitor_id is not None:
                teams_to_points_map[match.visitor_id][1] += match.visitor_points
        scoreboard = []
        for team in teams_queryset:
            points = teams_to_points_map[team.id]
            team.score = points[0] + points[1]
            team.score_as_visitor = points[1]
            scoreboard.append(team)
        scoreboard.sort(key=lambda team: (team.score, team.score_as_visitor), reverse=True)
        data = ScoreboardSerializer(scoreboard, many=True).data
        rest_response_data = OrderedDict(
            count=len(data),
            next=None,
            previous=None,
            results=data,
        )
        return Response(data=rest_response_data, status=status.HTTP_200_OK)

    @staticmethod
    def teams_queryset(league_id: int) -> QuerySet:
        return Team.objects.filter(league_id=league_id).all()

    def matches_with_points_queryset(self, league_id: int) -> QuerySet:
        return Match.objects.filter(league_id=league_id).annotate(
            host_points=Case(
                When(host_score__gt=F("visitor_score"), then=Value(self.POINTS_PER_WIN)),
                When(host_score=F("visitor_score"), then=Value(self.POINTS_PER_DRAW)),
                default=Value(self.POINTS_PER_LOSE),
            ),
            visitor_points=Case(
                When(visitor_score__gt=F("host_score"), then=Value(self.POINTS_PER_WIN)),
                When(visitor_score=F("host_score"), then=Value(self.POINTS_PER_DRAW)),
                default=Value(self.POINTS_PER_LOSE),
            ),
        )
