from rest_framework.response import Response
from rest_framework.decorators import api_view
from .crawl import CrawlNotice
from .department import get_department

department = get_department()

@api_view(['GET'])
def Showdata(request):
    
    data = CrawlNotice(department)
    
    return Response(data)