import sys
from django.core.management.base import BaseCommand, CommandError
from searcher.models import Person, Contribution, Motion, Question

class Command(BaseCommand):
    help = 'Returns the total number of table rows in the DB'

    def handle(self, *args, **options):
        sys.stdout.write('Counting rows...')
        persons = Person.objects.count()
        contribs = Contribution.objects.count()
        motions = Motion.objects.count()
        questions = Question.objects.count()
        print("""
{} people
{} contributions
{} motions
{} questions
{} total rows
""".format(persons, contribs, motions, questions,
        persons + contribs + motions + questions))