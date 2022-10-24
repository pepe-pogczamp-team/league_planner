from rest_framework import serializers

from league_planner.models.league import League


class LeagueSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = League
        fields = (
            "name",
        )
