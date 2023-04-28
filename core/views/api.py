import datetime

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from core import models, rest_serializers

@csrf_exempt
def batch(request, batch_name):
  """
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
  List all batches
  """
  if request.method == 'GET':
    batches = models.Batch.objects.all()
    serializer = rest_serializers.BatchesSerializer(batches, many=True, context={'request': request})
    return JsonResponse({'batches': serializer.data}, safe=False)
  else:
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  end

@csrf_exempt
def issue(request, lccn, date, edition):
  """
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
