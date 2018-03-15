from django.db import models
from django.utils import timezone
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex

class Person(models.Model):
    internal_id = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    is_msp = models.BooleanField(default=True)
    has_been_scraped = models.BooleanField(default=False)

    def __str__(self):
        return (self.name)

class Contribution(models.Model):
    internal_id = models.CharField(max_length=1024, blank=True, null=True)
    session = models.IntegerField(blank=True, null=True)
    meeting_type = models.CharField(max_length=1024, blank=True, null=True)
    heading_type = models.CharField(max_length=1024, blank=True, null=True)
    heading = models.CharField(max_length=1024, blank=True, null=True)
    subheading_type = models.CharField(max_length=1024, blank=True, null=True)
    subheading = models.CharField(max_length=1024, blank=True, null=True)
    party = models.CharField(max_length=1024, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    member = models.ForeignKey(Person, blank=True, null=True)
    member_office = models.CharField(max_length=1024, blank=True, null=True)
    has_been_scraped = models.BooleanField(default=False)

    def __str__(self):
        return (self.heading)

class Motion(models.Model):
    internal_id = models.CharField(max_length=256, blank=True, null=True)
    sp_ref = models.CharField(max_length=128, blank=True, null=True)
    sub_type = models.CharField(max_length=128, blank=True, null=True)
    member = models.ForeignKey(Person, blank=True, null=True)
    party = models.CharField(max_length=256, blank=True, null=True)
    date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    title = models.CharField(max_length=256, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    is_potential_mb = models.BooleanField(default=False)
    has_cross_party_support = models.BooleanField(default=False)
    has_been_scraped = models.BooleanField(default=False)
    search_vector = SearchVectorField(null=True)

    def __str__(self):
        return (self.title)

    class Meta(object):
        indexes = [GinIndex(fields=['search_vector'])]

class Question(models.Model):
    internal_id = models.CharField(max_length=256, blank=True, null=True)
    sp_ref = models.CharField(max_length=128, blank=True, null=True)
    sub_type = models.CharField(max_length=128, blank=True, null=True)
    member = models.ForeignKey(Person, blank=True, null=True)
    party = models.CharField(max_length=256, blank=True, null=True)
    date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    answer_date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    answer_text = models.TextField(blank=True, null=True)
    answered_by = models.CharField(max_length=256, blank=True, null=True)
    has_been_scraped = models.BooleanField(default=False)
    
    def __str__(self):
        return (self.sp_ref)