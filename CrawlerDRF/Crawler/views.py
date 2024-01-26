from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def Showdata(request):
    data = [
        {'category_id':'', 'title':'1', 'content':'', 'img_url':'', 'posted_at':'', 'deadline':''},
        {'category_id':'', 'title':'2', 'content':'', 'img_url':'', 'posted_at':'', 'deadline':''},
        {'category_id':'', 'title':'3', 'content':'', 'img_url':'', 'posted_at':'', 'deadline':''},
    ]
    serializer = data
    return Response(serializer)