from django.conf import settings
from django.urls import reverse
from rest_framework import serializers
from rfc3339 import rfc3339

from core import models

class BatchesSerializer(serializers.BaseSerializer):
  def to_representation(self, instance):
    return {
      'awardee': {
        'name': instance.awardee.name,
        'url': settings.BASE_URL + instance.awardee.json_url,
      },
      'ingested': rfc3339(instance.created),
      'lccns': instance.lccns(),
      'name': instance.name,
      'page_count': instance.page_count,
      'url': settings.BASE_URL + reverse('api_batch', args=[instance.name]),
    }

class BatchSerializer(serializers.BaseSerializer):
  def to_representation(self, instance):
    issues = []
    for issue in instance.issues.all():
      i = {
        'title': {
          'name': issue.title.display_name,
          'url': settings.BASE_URL + issue.title.json_url,
        },
        'date_issued': issue.date_issued.strftime('%Y-%m-%d'),
        'url': settings.BASE_URL + reverse('api_issue', args=[issue.title.lccn, issue.date_issued.strftime("%Y-%m-%d"), issue.edition])
      }
      issues.append(i)

    return {
      'awardee': {
        'name': instance.awardee.name,
        'url': settings.BASE_URL + instance.awardee.json_url,
      },
      'ingested': rfc3339(instance.created),
      'issues': issues,
      'lccns': instance.lccns(),
      'name': instance.name,
      'page_count': instance.page_count,
      'url': settings.BASE_URL + reverse('api_batch', args=[instance.name]),
    }

class IssueSerializer(serializers.BaseSerializer):
  def to_representation(self, instance):
    return {
      'batch': {
        'name': instance.batch.name,
        'url': settings.BASE_URL + reverse('api_batch', args=[instance.batch.name]),
      },
      'date_issued': instance.date_issued.strftime('%Y-%m-%d'),
      'edition': instance.edition,
      'number': instance.number,
      'title': {
        'name': instance.title.display_name,
        'url': settings.BASE_URL + instance.title.json_url
      },
      'url': settings.BASE_URL + reverse('api_issue', args=[instance.title.lccn, instance.date_issued.strftime("%Y-%m-%d"), instance.edition]),
      'volume': instance.volume,
    }
