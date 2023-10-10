from django.db.models.query import QuerySet
from django_filters.rest_framework import BaseInFilter, FilterSet


class IdsFilter(BaseInFilter):
    def filter(self, qs: QuerySet, ids: list[int]) -> QuerySet:  # noqa: A003
        return qs.filter(league__in=ids) if ids else qs


class FilterByLeague(FilterSet):
    league = IdsFilter(lookup_expr="exact")
