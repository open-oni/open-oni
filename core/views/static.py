from django.conf import settings
from django import urls
from django.http import HttpResponse
from core.models import Batch, Title, Issue, Page
from core.decorator import cache_page
from django.shortcuts import render
from django.template import RequestContext

@cache_page(settings.DEFAULT_TTL_SECONDS)
def about(request):
    page_title = "About " + settings.SITE_TITLE
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label':'About',
         'href': urls.reverse('openoni_about'),
         'active': True},
    ])
    return render(request, 'about.html', locals())

@cache_page(settings.DEFAULT_TTL_SECONDS)
def about_api(request):
    page_title = "About the Site and API"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label':'About API',
         'href': urls.reverse('openoni_about_api'),
         'active': True},
    ])
    batches = Batch.objects.all()
    batch = None
    lccn = None
    title = None
    issue = None
    page = None

    if len(batches) > 0:
      batch = batches[0]
      lccn = batch.lccns()[0]
      title = Title.objects.get(lccn=lccn)
      issue = title.issues.all()[0]
      page = issue.pages.all()[0]

    return render(request, 'about_api.html', locals())

def empty(request, *args, **kwargs):
    return HttpResponse(status=204)

@cache_page(settings.DEFAULT_TTL_SECONDS)
def help(request):
    page_title = "Help"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label':'Help',
         'href': urls.reverse('openoni_help'),
         'active': True},
    ])
    return render(request, 'help.html', locals())
