from django.conf import settings
from django.urls import reverse
from rest_framework import serializers
from rfc3339 import rfc3339

from core import models


class AwardeeListSerializer(serializers.BaseSerializer):
    """
    api/chronam/awardees.json
    List all awardees
    """

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'url': settings.BASE_URL + reverse('api_chronam_awardee', args=[instance.org_code]),
        }


class AwardeeSerializer(serializers.BaseSerializer):
    """
    api/chronam/awardee/<org_code>.json
    Retrieve an awardee and its batches
    """

    def to_representation(self, instance):
        return {
            'batches': [{
                'name': batch.name,
                'url': settings.BASE_URL + reverse('api_chronam_batch', args=[batch.name]),
            } for batch in models.Batch.objects.filter(awardee=instance)],
            'name': instance.name,
            'url': settings.BASE_URL + reverse('api_chronam_awardee', args=[instance.org_code]),
        }


class BatchListSerializer(serializers.BaseSerializer):
    """
    api/chronam/batches.json; api/chronam/batches/<page_number>.json
    List all batches
    """

    def to_representation(self, instance):
        return {
            'awardee': {
                'name': instance.awardee.name,
                'url': settings.BASE_URL + reverse('api_chronam_awardee', args=[instance.awardee.org_code]),
            },
            'ingested': rfc3339(instance.created),
            'lccns': instance.lccns(),
            'name': instance.name,
            'page_count': instance.page_count,
            'url': settings.BASE_URL + reverse('api_chronam_batch', args=[instance.name]),
        }


class BatchSerializer(serializers.BaseSerializer):
    """
    api/chronam/batches/<batch_name>.json
    Retrieve a batch and its issues
    """

    def to_representation(self, instance):
        return {
            'awardee': {
                'name': instance.awardee.name,
                'url': settings.BASE_URL + instance.awardee.json_url,
            },
            'ingested': rfc3339(instance.created),
            'issues': [{
                'date_issued': issue.date_issued.strftime('%Y-%m-%d'),
                'title': {
                    'name': issue.title.display_name,
                    'url': settings.BASE_URL + reverse('api_chronam_title', args=[issue.title.lccn]),
                },
                'url': settings.BASE_URL + reverse('api_chronam_issue', args=[
                    issue.title.lccn,
                    issue.date_issued.strftime("%Y-%m-%d"),
                    issue.edition
                ]),
            } for issue in instance.issues.all()],
            'lccns': instance.lccns(),
            'name': instance.name,
            'page_count': instance.page_count,
            'url': settings.BASE_URL + reverse('api_chronam_batch', args=[instance.name]),
        }


class IssueSerializer(serializers.BaseSerializer):
    """
    api/chronam/lccn/<date>/ed-<edition>.json
    Retrieve an issue's info
    """

    def to_representation(self, instance):
        return {
            'batch': {
                'name': instance.batch.name,
                'url': settings.BASE_URL + reverse('api_chronam_batch', args=[instance.batch.name]),
            },
            'date_issued': instance.date_issued.strftime('%Y-%m-%d'),
            'edition': instance.edition,
            'number': instance.number,
            'pages': [{
                'sequence': p.sequence,
                'url': settings.BASE_URL + reverse('api_chronam_page', args=[
                    p.issue.title.lccn,
                    p.issue.date_issued.strftime("%Y-%m-%d"),
                    p.issue.edition, p.sequence
                ]),
            } for p in instance.pages.all()],
            'title': {
                'name': instance.title.display_name,
                'url': settings.BASE_URL + reverse('api_chronam_title', args=[instance.title.lccn]),
            },
            'url': settings.BASE_URL + reverse('api_chronam_issue', args=[
                instance.title.lccn,
                instance.date_issued.strftime("%Y-%m-%d"),
                instance.edition
            ]),
            'volume': instance.volume,
        }


class NewspaperListSerializer(serializers.BaseSerializer):
    """
    api/chronam/newspapers.json
    List all newspapers
    """

    def to_representation(self, instance):
        newspapers = []
        for state, titles in instance:
            for title in titles:
                newspapers.append({
                    'lccn': title.lccn,
                    'state': state,
                    'title': title.display_name,
                    'url': settings.BASE_URL + reverse('api_chronam_title', args=[title.lccn]),
                })
        return newspapers


class PageSerializer(serializers.BaseSerializer):
    """
    api/chronam/lccn/<date>/ed-<edition>/seq-<sequence>.json
    Retrieve a page's info
    """

    def to_representation(self, instance):
        return {
            'issue': {
                'date_issued': instance.issue.date_issued.strftime("%Y-%m-%d"),
                'url': settings.BASE_URL + reverse('api_chronam_issue', args=[
                    instance.issue.title.lccn,
                    instance.issue.date_issued.strftime("%Y-%m-%d"),
                    instance.issue.edition
                ]),
            },
            'jp2': settings.BASE_URL + instance.jp2_url,
            'ocr': settings.BASE_URL + instance.ocr_url,
            'pdf': settings.BASE_URL + instance.pdf_url,
            'sequence': instance.sequence,
            'text': settings.BASE_URL + instance.txt_url,
            'title': {
                'name': instance.issue.title.display_name,
                'url': settings.BASE_URL + reverse('api_chronam_title', args=[instance.issue.title.lccn]),
            },
        }


class TitleSerializer(serializers.BaseSerializer):
    """
    api/chronam/lccn/<lccn>.json
    Retrieve a title's info
    """

    def to_representation(self, instance):
        return {
            'end_year': instance.end_year,
            'issues': [{
                'url': settings.BASE_URL + reverse('api_chronam_issue', args=[
                    i.title.lccn,
                    i.date_issued.strftime("%Y-%m-%d"),
                    i.edition
                ]),
                'date_issued': i.date_issued.strftime("%Y-%m-%d"),
            } for i in instance.issues.all()],
            'lccn': instance.lccn,
            'name': instance.display_name,
            'place': [p.name for p in instance.places.all()],
            'place_of_publication': instance.place_of_publication,
            'publisher': instance.publisher,
            'start_year': instance.start_year,
            'subject': [s.heading for s in instance.subjects.all()],
            'url': settings.BASE_URL + reverse('api_chronam_title', args=[instance.lccn]),
        }
