from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg

from movies.models import FilmWork, PersonRole


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def _aggregate_person(role: str):
        return ArrayAgg(
            'personfilmwork__person__full_name',
            filter=Q(personfilmwork__role=role),
            distinct=True,
        )

    @classmethod
    def get_queryset(cls):
        return FilmWork.objects.values('id', 'title', 'description', 'creation_date', 'rating', 'type'
                ).annotate(
                    genres=ArrayAgg('genres__name', distinct=True),
                    actors=cls._aggregate_person(role=PersonRole.ACTOR),
                    directors=cls._aggregate_person(role=PersonRole.DIRECTOR),
                    writers=cls._aggregate_person(role=PersonRole.WRITER)
        )

    @staticmethod
    def render_to_response(context, **response_kwargs):
        return JsonResponse(context)


class Movies(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            self.get_queryset(),
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)['object']
