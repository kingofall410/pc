from django.http.response import HttpResponse
from . import scraper
import time
from django.db import transaction

@transaction.atomic
def scraperview(request):
    start = time.time()
    scraper.load()
    return HttpResponse((time.time()-start))
