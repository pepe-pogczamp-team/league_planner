from rest_framework import serializers

from league_planner.models.league import League
from league_planner.models.match import Match
from league_planner.models.team import Team


class MatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    league = serializers.PrimaryKeyRelatedField(queryset=League.objects.all())
    host = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        required=False,
    )
    visitor = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        required=False,
    )
    host_score = serializers.IntegerField(required=False)
    visitor_score = serializers.IntegerField(required=False)
    address = serializers.CharField(
        max_length=50,
        required=False,
    )
    datetime = serializers.DateTimeField(required=False)

    class Meta:
        model = Match
        fields = (
            "id",
            "league",
            "host",
            "host_score",
            "visitor",
            "visitor_score",
            "address",
            "datetime",
        )
