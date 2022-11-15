from rest_framework import serializers

from league_planner.models.league import League
from league_planner.models.team import Team


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    league = serializers.PrimaryKeyRelatedField(queryset=League.objects.all())
    name = serializers.CharField()
    city = serializers.CharField(required=False)

    class Meta:
        model = Team
        fields = ("id", "league", "name", "city")
