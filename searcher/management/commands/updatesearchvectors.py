from django.core.management.base import BaseCommand, CommandError
from django.contrib.postgres.search import SearchVector
from searcher.models import Contribution, Motion, Question

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Updating search vectors...')
        Motion.objects.update(search_vector=SearchVector('title', 'text'))
        Contribution.objects.update(search_vector=SearchVector('heading', 'subheading', 'text'))
        Question.objects.update(search_vector=SearchVector('text', 'answer_text'))