import sys
import requests
import datetime
from django.utils.dateparse import parse_datetime
from django.core.management.base import BaseCommand, CommandError
from searcher.models import Person, Contribution, Motion, Question
from django.core.management import call_command

class Command(BaseCommand):
    MIN_CHARS_FOR_ENTRY = 128
    help = 'Gets historical data from the SP APIs'
    CONTRIB_YEARS = ['2012','2013', '2014', '2015', '2016', '2017']

    CONTRIB_FULL_YEARS = [
        '1999', '2000', '2001', '2002', '2003',
        '2004','2005', '2006', '2007', '2008',
        '2009', '2010', '2011', '2012','2013',
        '2014', '2015', '2016', '2017'
        ]


    def get_person(self, p_id, p_name):
        try:
            if(p_id is not 0): person = Person.objects.get(internal_id=p_id)
            else: person = Person.objects.get(name=p_name)
            return person
        except:
            if(p_id is not 0): is_msp = True
            else: is_msp = False
            return Person(
                internal_id = p_id,
                name = p_name,
                is_msp = is_msp
                )

    def create_contribution(self, contrib_obj, is_committee):
        if is_committee is False:
            heading_type = contrib_obj['Heading_Type']
            subheading_type = contrib_obj['Sub_Heading_Type']
        else:
            heading_type = None
            subheading_type = None
        if (contrib_obj and len(contrib_obj['Edited_Text']) >= self.MIN_CHARS_FOR_ENTRY):
            if (contrib_obj['Submitted_Date']):
                date = parse_datetime(contrib_obj['Submitted_Date'])
            else: date = None
            return Contribution(
                internal_id = contrib_obj['ID'],
                session = int(contrib_obj['Session']),
                meeting_type = contrib_obj['Meeting_Type'],
                heading_type = heading_type,
                heading = contrib_obj['Heading'],
                subheading_type = subheading_type,
                subheading = contrib_obj['Sub_Heading'],
                party = contrib_obj['Actual_Party_Name'],
                text = contrib_obj['Edited_Text'],
                date = date,
                member = self.get_person(contrib_obj['Person_ID'], contrib_obj['Parliamentary_Name']),
                member_office = contrib_obj['Speaker_Office'],
                has_been_scraped = False
            )
        else: return False

    def add_contributions(self, is_committee):
        if is_committee:
            endpoint = 'https://data.parliament.scot/api/orscommitteemeeting'
            print('Getting Committee contributions...')
        else:
            endpoint = 'https://data.parliament.scot/api/orsplenarymeeting'
            print('Getting Plenary contributions...')
        for year in self.CONTRIB_YEARS:
            params = {'year': year}
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                print('Got data for {}'.format(year))
                resArr = response.json()
                contribs_to_add = []
                for i, contrib_obj in enumerate(resArr):
                    sys.stdout.write('Processing {} of {}   \r'.format(i, len(resArr) - 1))
                    sys.stdout.flush()
                    try:
                        newContrib = self.create_contribution(contrib_obj, is_committee)
                        if newContrib: contribs_to_add.append(newContrib)
                    except:
                        print('Error adding contribution:')
                        print(contrib_obj)
                        break
                sys.stdout.write('\r\n')
                print('Adding to DB...')
                Contribution.objects.bulk_create(contribs_to_add)
            else: print('Error getting data for {}'.format(year))

    def create_motion(self, motion_obj, sub_types):
        if (motion_obj):
            if (motion_obj['SubmissionDateTime']):
                date = parse_datetime(motion_obj['SubmissionDateTime'])
            else: date = None
            return Motion(
                internal_id = motion_obj['UniqueID'],
                sp_ref = motion_obj['EventID'],
                sub_type = sub_types[motion_obj['EventSubTypeID']],
                member = self.get_person(motion_obj['MSPID'], ''),
                party = motion_obj['Party'],
                date = date,
                title = motion_obj['Title'],
                text = motion_obj['ItemText'],
                is_potential_mb = motion_obj['ConsideredForMembersBusiness'],
                has_cross_party_support = motion_obj['CrossPartySupport'],
                has_been_scraped = False
            )
        else: return False

    def add_motions(self, sub_types):
        print('Getting motions...')
        endpoint = 'https://data.parliament.scot/api/motionsquestionsanswersmotions'
        response = requests.get(endpoint)
        motions_to_add = []
        if response.status_code == 200:
            print('Got motion data...')
            resArr = response.json()
            for i, motion_obj in enumerate(resArr):
                sys.stdout.write('Processing {} of {}   \r'.format(i, len(resArr) - 1))
                sys.stdout.flush()
                new_motion = self.create_motion(motion_obj, sub_types)
                if new_motion: motions_to_add.append(new_motion)
            sys.stdout.write('\r\n')
            print('Adding to DB...')
            Motion.objects.bulk_create(motions_to_add)
        else: print('Error getting Motion data')

    def create_question(self, question_obj, sub_types):
        if (question_obj):
            if (question_obj['SubmissionDateTime']):
                date = parse_datetime(question_obj['SubmissionDateTime'])
            else: date = None
            if (question_obj['AnswerDate']):
                answer_date = parse_datetime(question_obj['AnswerDate'])
            else: answer_date = None
            return Question(
                internal_id = question_obj['UniqueID'],
                sp_ref = question_obj['EventID'],
                sub_type = sub_types[question_obj['EventSubTypeID']],
                member = self.get_person(question_obj['MSPID'], ''),
                party = question_obj['Party'],
                date = date,
                answer_date = answer_date,
                text = question_obj['ItemText'],
                answer_text = question_obj['AnswerText'],
                answered_by = question_obj['AnsweredByMSP'],
                has_been_scraped = False
            )
        else: return False

    def add_questions(self, sub_types):
        endpoint = 'https://data.parliament.scot/api/motionsquestionsanswersquestions'
        print('Getting questions...')
        for year in self.CONTRIB_YEARS:
            params = {'year': year}
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                print('Got data for {}'.format(year))
                resArr = response.json()
                questions_to_add = []
                for i, question_obj in enumerate(resArr):
                    sys.stdout.write('Processing {} of {}   \r'.format(i, len(resArr) - 1))
                    sys.stdout.flush()
                    new_question = self.create_question(question_obj, sub_types)
                    if new_question: questions_to_add.append(new_question)
                sys.stdout.write('\r\n')
                print('Adding to DB...')
                Question.objects.bulk_create(questions_to_add)
            else: print('Error getting data for {}'.format(year))

    def get_sub_types_dict(self):
        print('Getting item subtypes...')
        endpoint = 'https://data.parliament.scot/api/motionsquestionsanswerseventsubtypes'
        response = requests.get(endpoint)
        sub_types_tuples = []
        if response.status_code == 200:
            resArr = response.json()
            for sub_type in resArr:
                sub_types_tuples.append((sub_type['EventSubTypeID'], sub_type['EventSubType']))
            return dict(sub_types_tuples)
        else:
            print('Error getting subtypes')
            return None

    def add_MSPs(self):
        print('Getting MSP data...')
        endpoint = 'https://data.parliament.scot/api/members'
        response = requests.get(endpoint)
        persons_to_add = []
        if response.status_code == 200:
            resArr = response.json()
            for p in resArr:
                persons_to_add.append(self.get_person(p['PersonID'], p['ParliamentaryName']))
            Person.objects.bulk_create(persons_to_add)
        else: print('Error getting MSP data')


    def handle(self, *args, **options):
        call_command('deleteall')
        self.add_MSPs()
        # MSP data should exist
        #self.add_contributions(False)
        #self.add_contributions(True)
        sub_types = self.get_sub_types_dict()
        # Sub type data should exist
        self.add_questions(sub_types)
        self.add_motions(sub_types)
        call_command('updatesearchvectors')
        print('Done!')