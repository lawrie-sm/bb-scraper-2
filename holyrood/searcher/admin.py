from django.contrib import admin
from .models import Person, Contribution, Motion, Question

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = (
        'heading',
        'date',
        'member',
        'subheading'
        )
    list_filter = (
        'meeting_type',
        'heading_type',
        'session',
        'date',
        'member',
        'has_been_scraped'
    )
    fields = (
        'internal_id', 'has_been_scraped',
        ( 'date', 'session' ),
        'meeting_type',
        ( 'heading', 'heading_type' ),
        ('subheading' , 'subheading_type' ),
        ('member', 'member_office', 'party'),
        'text',
        'search_vector'
    )
    readonly_fields = (
        'internal_id', 'date', 'session', 'meeting_type',
        'heading', 'heading_type', 'subheading', 'subheading_type',
        'member', 'member_office', 'party', 'text', 'has_been_scraped'
    )

class PersonAdminInline(admin.TabularInline):
    model = Contribution
    fields = (
        'date',
        'text'
    )
    readonly_fields = (
        'internal_id', 'date', 'session', 'meeting_type',
        'heading', 'heading_type', 'subheading', 'subheading_type',
        'member', 'member_office', 'party', 'text'
    )
    extra = 0

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('internal_id', 'name', 'is_msp')
    inlines = (PersonAdminInline, )



@admin.register(Motion)
class MotionAdmin(admin.ModelAdmin):
    list_display = (
        'sp_ref',
        'title',
        'date',
        'member',
    )
    list_filter = (
        'party',
        'date',
        'member',
        'has_been_scraped'
    )
    fields = (
        ('sp_ref', 'sub_type', 'internal_id', 'has_been_scraped'),
        ('title', 'date'),
        ('member', 'party'),
        ('is_potential_mb', 'has_cross_party_support'),
        'text',
        'search_vector'
    )
    readonly_fields = (
        'title', 'date', 'member', 'party',
        'internal_id', 'sp_ref', 'sub_type',
        'is_potential_mb', 'has_cross_party_support', 'text',
        'has_been_scraped',
    )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'sp_ref',
        'date',
        'member'
    )
    list_filter = (
        'party',
        'date', 
        'member',
        'answered_by',
        'has_been_scraped',
    )
    fields = (
        ('sp_ref', 'sub_type', 'internal_id', 'has_been_scraped'),
        ('date', 'answer_date'),
        ('member', 'party', 'answered_by'),
        'text',
        'answer_text',
        'search_vector'
    )
    readonly_fields = (
        'date', 'member', 'party',
        'internal_id', 'sp_ref', 'sub_type',
        'answer_date', 'answered_by',
        'text', 'answer_text', 'has_been_scraped',
    )