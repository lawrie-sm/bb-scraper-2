from django.core import serializers
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from searcher.models import Contribution, Motion, Question
from itertools import chain
import datetime

class index(View):
    def get(self, request):
        return render(request, 'searcher/index.html')

class SPSearchResults(ListView):
    def get(self, request):
        if (request.GET['q'] is not None):
            keywords = request.GET['q']
            query = SearchQuery(keywords)

            date_range = request.GET['date-range']
            # Temp date set to 2016
            current_date = datetime.date(2016, 1, 1)
            start_date = datetime.date(1999, 6, 1)
            if (date_range == 'last-year'):
                start_date = current_date - datetime.timedelta(days=365.24)
            elif (date_range == 'last-5-years'):
                start_date = current_date - datetime.timedelta(days=(365.24*5))
            elif (date_range == 'last-10-years'):
                start_date = current_date - datetime.timedelta(days=(365.24*10))


            cont = (request.GET['cont'] is not None)
            mot = (request.GET['mot'] is not None)
            qs = (request.GET['qs'] is not None)
            snp = (request.GET['snp'] is not None)
            lab = (request.GET['lab'] is not None)
            con = (request.GET['con'] is not None)
            ld = (request.GET['ld'] is not None)
            grn = (request.GET['grn'] is not None)
            oth = (request.GET['oth'] is not None)

            
            motions_queryset = Motion.objects.filter(search_vector=query, date__gte=start_date)
            # questions_queryset = Question.objects.filter(search_vector=query)
            full_queryset = motions_queryset # chain(motions_queryset, questions_queryset)

            # TODO: Use "values" after the filter to speed up, run date and type search through this

            data_json = serializers.serialize('json', full_queryset)
            context = {
                'data_json': data_json
            }

        return render(request, 'searcher/results.html', context=context)