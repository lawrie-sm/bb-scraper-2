from django.core import serializers
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from searcher.models import Contribution, Motion, Question
from itertools import chain

class index(View):
    def get(self, request):
        return render(request, 'searcher/index.html')

class SPSearchResults(ListView):
    def get(self, request):
        if (request.GET['q'] is not None):
            keywords = request.GET['q']
            query = SearchQuery(keywords)
            motions_queryset = Motion.objects.filter(search_vector=query)
            contribs_queryset = Contribution.objects.filter(search_vector=query)
            questions_queryset = Question.objects.filter(search_vector=query)
            
            full_queryset = chain(motions_queryset, contribs_queryset, questions_queryset)

            data_json = serializers.serialize('json', full_queryset)
            context = {
                'data_json': data_json
            }

        return render(request, 'searcher/results.html', context=context)