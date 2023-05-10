import datetime

from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core import models, rest_serializers

@api_view(['GET'])
def awardee(request, org_code):
  """
  api/oni/awardee/<org_code>.json
  Retrieve an awardee and its batches
  """
  awardee = models.Awardee.objects.get(org_code=org_code)
  serializer = rest_serializers.AwardeeSerializer(awardee, context={'request': request})
  return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def awardee_list(request):
  """
  api/oni/awardees.json
  List all awardees
  """
  awardees = models.Awardee.objects.all()
  serializer = rest_serializers.AwardeeListSerializer(awardees, many=True, context={'request': request})
  return JsonResponse({'awardees': serializer.data}, safe=False)

@api_view(['GET'])
def batch(request, batch_name):
  """
  api/oni/batches/<batch_name>.json
  Retrieve a batch and its issues
  """
  batch = models.Batch.objects.get(name=batch_name)
  serializer = rest_serializers.BatchSerializer(batch, context={'request': request})
  return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def batch_list(request, page_number=1):
  """
  api/oni/batches.json
  List all batches
  """
  batches = models.Batch.objects.all()
  paginator = Paginator(batches, 25)
  page = paginator.page(page_number)
  serializer = rest_serializers.BatchListSerializer(page.object_list, many=True, context={'request': request})
  data = {
    'batches': serializer.data,
    'count': paginator.count,
    'pages': paginator.num_pages,
  }
  if page.has_next():
    data['next'] = settings.BASE_URL + reverse('api_batch_list_page', args=[page.next_page_number()])
  if page.has_previous():
    data['previous'] = settings.BASE_URL + reverse('api_batch_list_page', args=[page.previous_page_number()])

  return JsonResponse(data, safe=False)

@api_view(['GET'])
def issue(request, lccn, date, edition):
  """
  api/oni/lccn/<date>/ed-<edition>.json
  Retrieve an issue's info
  """
  _year, _month, _day = date.split("-")
  _date = datetime.date(int(_year), int(_month), int(_day))
  title = models.Title.objects.get(lccn=lccn)
  issue = title.issues.filter(date_issued=_date, edition=edition).order_by("-created")[0]
  serializer = rest_serializers.IssueSerializer(issue, context={'request': request})
  return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def newspaper_list(request):
  """
  api/oni/newspapers.json
  List all newspapers
  """
  _newspapers_by_state = {}
  for title in models.Title.objects.filter(has_issues=True).prefetch_related('places'):
    for place in title.places.all():
      if place.state:
        _newspapers_by_state.setdefault(place.state, set()).add(title)
  states_with_newspapers = [
    (s, sorted(t, key=lambda title: title.name_normal))
    for s, t in sorted(_newspapers_by_state.items())
  ]
  serializer = rest_serializers.NewspaperListSerializer(states_with_newspapers, context={'request': request})
  return JsonResponse({'newspapers': serializer.data}, safe=False)

@api_view(['GET'])
def page(request, lccn, date, edition, sequence):
  """
  api/oni/lccn/<date>/ed-<edition>/seq-<sequence>.json
  Retrieve a page's info
  """
  _year, _month, _day = date.split("-")
  _date = datetime.date(int(_year), int(_month), int(_day))
  title = models.Title.objects.get(lccn=lccn)
  issue = title.issues.filter(date_issued=_date, edition=edition).order_by("-created")[0]
  page = issue.pages.filter(sequence=int(sequence)).order_by("-created")[0]
  serializer = rest_serializers.PageSerializer(page, context={'request': request})
  return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def title(request, lccn):
  """
  api/oni/lccn/<lccn>.json
  Retrieve a title's info
  """
  title = models.Title.objects.get(lccn=lccn)
  serializer = rest_serializers.TitleSerializer(title, context={'request': request})
  return JsonResponse(serializer.data, safe=False)
