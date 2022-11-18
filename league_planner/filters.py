from django_filters.rest_framework import FilterSet, BaseInFilter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from django.db.models.query import QuerySet


class IdsFilter(BaseInFilter):
    def filter(self, qs: "QuerySet", ids: "List[int]") -> "QuerySet":
        return qs.filter(league__in=ids) if ids else qs


class FilterByLeague(FilterSet):
    league = IdsFilter(lookup_expr="exact")
