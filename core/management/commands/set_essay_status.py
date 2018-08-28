# functionality to display "has more info" on papers was removed in openoni core
# as well as storing the essays in the database itself
# this script will return the ability to detect essays with title.essay should
# users choose to use it after they add essays or titles

import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.views.generic import TemplateView

from core.models import Title

class Command(BaseCommand):
    help = "Checks essays in "+settings.ESSAY_TEMPLATES+" and sets value in database"

    def handle(self, *args, **options):

        print "Pulling from location across apps:  <app>/templates/"+settings.ESSAY_TEMPLATES
        titles = Title.objects.all()
        for title in titles:
            try:
                template = os.path.join(settings.ESSAY_TEMPLATES, title.lccn+".html")
                get_template(template)
                # if you've gotten this far, then the template was found
                title.essay = True
            except TemplateDoesNotExist:
                title.essay = False
            title.save()

        with_essays = Title.objects.filter(essay=True)
        without_essays = Title.objects.filter(essay=False)

        print "\nTitles With Essays ("+str(len(with_essays))+"):"
        for title in with_essays:
            print "    "+title.name
        
        print "\nTitles Without Essays ("+str(len(without_essays))+"):"
        for title in without_essays:
            print "    "+title.name
