from typing import TYPE_CHECKING

from rest_framework import permissions

from league_planner.models.league import League

if TYPE_CHECKING:
    from django.contrib.auth.models import User
    from rest_framework.viewsets import GenericViewSet
    from typing import Any, Self
    from rest_framework.request import Request


class IsLeagueOwner(permissions.BasePermission):
    def has_object_permission(
        self: "Self",
        request: "Request",
        view: "GenericViewSet",
        league: "League",
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return self.is_owner(request.user, league)

    @staticmethod
    def is_owner(user: "User", league: "League") -> bool:
        return user == league.owner


class IsLeagueResourceOwner(IsLeagueOwner):
    @staticmethod
    def is_owner(user: "User", obj: "Any") -> bool:
        return user == obj.league.owner

    def has_permission(
        self: "Self",
        request: "Request",
        view: "GenericViewSet",
    ) -> bool:
        if request.method == "POST":
            league = League.objects.get(id=request.data.get("league"))
            if request.user != league.owner:
                return False
        return super().has_permission(request, view)
