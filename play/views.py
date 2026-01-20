from django.shortcuts import render
from .tasks import notify_user
import requests
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator 
from rest_framework.views import APIView
#from django.contrib.contenttypes.fields import GenericForeignKey
import logging

# Create your views here.
logger = logging.getLogger(__name__)

class HelloView(APIView):
    
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('httpbin response received')
            data = response.json
        except requests.ConnectionError:
            logger.critical('httpbin is down')
        return render(request, 'play/hello.html', {'name': data})






    

