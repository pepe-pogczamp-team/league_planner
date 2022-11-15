from rest_framework import viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from league_planner.models.team import Team
from league_planner.pagination import Pagination
from league_planner.serializers.team import TeamSerializer


class TeamViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = Pagination
