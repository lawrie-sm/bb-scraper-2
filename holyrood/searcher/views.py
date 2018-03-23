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
        req = request.GET
        if ('q' in req and 'date-range' in req):
            keywords = req['q']
            query = SearchQuery(keywords)
            date_range = req['date-range']
            # Temp date set to 2016
            current_date = datetime.date(2016, 1, 1)
            start_date = datetime.date(1999, 6, 1)
            if (date_range == 'last-year'):
                start_date = current_date - datetime.timedelta(days=365.24)
            elif (date_range == 'last-5-years'):
                start_date = current_date - datetime.timedelta(days=(365.24*5))
            elif (date_range == 'last-10-years'):
                start_date = current_date - datetime.timedelta(days=(365.24*10))

            print(request.GET)

            # TODO: Could refactor form to be tidier or use reflection here
            snp = False
            lab = False
            con = False
            ld = False
            grn = False
            oth = False
            cont = False
            qs = False
            mot = False
            if ('snp' in req): snp = True
            if ('lab' in req): lab = True
            if ('con' in req): con = True
            if ('ld' in req): ld = True
            if ('grn' in req): grn = True
            if ('oth' in req): oth = True
            if ('cont' in req): cont = True
            if ('qs' in req): qs = True
            if ('mot' in req): mot = True

            full_qs_list = []
            
            if (mot):
                mot_qs = Motion.objects.filter(search_vector=query, date__gte=start_date)
                full_qs_list.append(mot_qs)
            if (qs):
                qs_qs = Question.objects.filter(search_vector=query, date__gte=start_date)
                full_qs_list.append(qs_qs)

            full_queryset = chain.from_iterable(full_qs_list)

            # TODO: Use "values" after the filter to speed up, run date and type search through this

            data_json = serializers.serialize('json', full_queryset)
            context = {
                'data_json': data_json
            }

        return render(request, 'searcher/results.html', context=context)