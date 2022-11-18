from rest_framework import viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from league_planner.filters import FilterByLeague
from league_planner.models.match import Match
from league_planner.pagination import Pagination
from league_planner.serializers.match import MatchSerializer


class MatchViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    pagination_class = Pagination
    filterset_class = FilterByLeague
