from django.core.management.base import BaseCommand, CommandError
from searcher.models import Person, Contribution, Motion, Question

class Command(BaseCommand):
    help = 'Deletes all non-scraped contributions'

    def handle(self, *args, **options):
        print('Clearing DB of non-scraped data...')
        non_scraped_items = Contribution.objects.filter(has_been_scraped=False)
        while non_scraped_items.count():
            ids = non_scraped_items.values_list('pk', flat=True)[:100]
            non_scraped_items.filter(pk__in = ids).delete()

        non_scraped_items = Person.objects.filter(has_been_scraped=False)
        while Person.objects.count():
            ids = non_scraped_items.values_list('pk', flat=True)[:100]
            non_scraped_items.filter(pk__in = ids).delete()

        non_scraped_items = Motion.objects.filter(has_been_scraped=False)
        while Motion.objects.count():
            ids = non_scraped_items.values_list('pk', flat=True)[:100]
            non_scraped_items.filter(pk__in = ids).delete()

        non_scraped_items = Question.objects.filter(has_been_scraped=False)
        while Question.objects.count():
            ids = non_scraped_items.values_list('pk', flat=True)[:100]
            non_scraped_items.filter(pk__in = ids).delete()