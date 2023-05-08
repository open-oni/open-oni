import datetime

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from core import models, rest_serializers

@csrf_exempt
def awardee(request, org_code):
  """
  api/oni/awardee/<org_code>.json
  Retrieve an awardee and its batches
  """
  if request.method == 'GET':
    awardee = models.Awardee.objects.get(org_code=org_code)
    serializer = rest_serializers.AwardeeSerializer(awardee, context={'request': request})
    return JsonResponse(serializer.data, safe=False)
  else:
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  end

@csrf_exempt
def awardee_list(request):
  """
  api/oni/awardees.json
  List all awardees
  """
  if request.method == 'GET':
    awardees = models.Awardee.objects.all()
    serializer = rest_serializers.AwardeeListSerializer(awardees, many=True, context={'request': request})
    return JsonResponse({'awardees': serializer.data}, safe=False)
  else:
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  end

@csrf_exempt
def batch(request, batch_name):
  """
  api/oni/batches/<batch_name>.json
  Retrieve a batch and its issues
  """
  if request.method == 'GET':
    batch = models.Batch.objects.get(name=batch_name)
    serializer = rest_serializers.BatchSerializer(batch, context={'request': request})
    return JsonResponse(serializer.data, safe=False)
  else:
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  end

@csrf_exempt
def batch_list(request):
  """
  api/oni/batches.json
  List all batches
  """
  if request.method == 'GET':
    batches = models.Batch.objects.all()
    serializer = rest_serializers.BatchListSerializer(batches, many=True, context={'request': request})
    return JsonResponse({'batches': serializer.data}, safe=False)
  else:
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  end

@csrf_exempt
def issue(request, lccn, date, edition):
  """
  api/oni/lccn/<date>/ed-<edition>.json
  Retrieve an issue's info
  """
  if request.method == 'GET':
    _year, _month, _day = date.split("-")
    _date = datetime.date(int(_year), int(_month), int(_day))
    title = models.Title.objects.get(lccn=lccn)
    issue = title.issues.filter(date_issued=_date, edition=edition).order_by("-created")[0]
    serializer = rest_serializers.IssueSerializer(issue, context={'request': request})
    return JsonResponse(serializer.data, safe=False)
  else:
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  end

@csrf_exempt
def newspaper_list(request):
  """
  api/oni/newspapers.json
  List all newspapers
  """
  if request.method == 'GET':
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
  else:
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  end

@csrf_exempt
def page(request, lccn, date, edition, sequence):
  """
  api/oni/lccn/<date>/ed-<edition>/seq-<sequence>.json
  Retrieve a page's info
  """
  if request.method == 'GET':
    _year, _month, _day = date.split("-")
    _date = datetime.date(int(_year), int(_month), int(_day))
    title = models.Title.objects.get(lccn=lccn)
    issue = title.issues.filter(date_issued=_date, edition=edition).order_by("-created")[0]
    page = issue.pages.filter(sequence=int(sequence)).order_by("-created")[0]
    serializer = rest_serializers.PageSerializer(page, context={'request': request})
    return JsonResponse(serializer.data, safe=False)
  else:
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  end


@csrf_exempt
def title(request, lccn):
  """
  api/oni/lccn/<lccn>.json
  Retrieve a title's info
  """
  if request.method == 'GET':
    title = models.Title.objects.get(lccn=lccn)
    serializer = rest_serializers.TitleSerializer(title, context={'request': request})
    return JsonResponse(serializer.data, safe=False)
  else:
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  end
