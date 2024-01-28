from rest_framework.response import Response
from rest_framework.decorators import api_view
from .crawl import CrawlNotice

@api_view(['GET'])
def Showdata(request):
    
    data = CrawlNotice('isis', 376)
    
    return Response(data)