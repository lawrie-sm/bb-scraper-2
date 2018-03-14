from django.core import serializers
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from searcher.forms import SPSearchForm
from searcher.models import Contribution, Motion, Question


class index(View):
    def get(self, request):
        search_form = SPSearchForm()
        return render(request, 'searcher/index.html', {'search_form': search_form})

class SPSearchResults(ListView):
    def get(self, request):
        search_form = SPSearchForm()
        if (request.GET['q'] is not None):
            queryset = Motion.objects
            keywords = request.GET['q']
            query = SearchQuery(keywords)
            vector = SearchVector('title', 'text')
            queryset = queryset.annotate(search=vector).filter(search=query)
            queryset = queryset.annotate(rank=SearchRank(vector, query)).order_by('-rank')
            json = serializers.serialize('json', queryset)
            context = {
                'search_form': search_form,
                'motions': queryset,
                'motions_json': json
            }

        return render(request, 'searcher/results.html', context=context)