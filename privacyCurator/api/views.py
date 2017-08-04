from rest_framework import generics, permissions
from api.models import Visit, Source
from api.serializers import VisitSerializer, UserSerializer, SourceSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404

from . import modelHandler

class VisitList(generics.ListCreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
    def perform_create(self, serializer):
        modelHandler.addOrUpdateVisit(serializer)
        #serializer.save(user=self.request.user);

class SubmitVisit(APIView):
    
    def get_object(self, d):
        #print(d)
        try:
            print("trying")
            #for source in list(Source.objects.all()):
             #   print(source.domain)
            s = Source.objects.filter(domain="http://www.thejustice.org/ ")
            print(len(s))
            for source in s:
                print(source)
            #print(s.domain)
        except Source.DoesNotExist:
            print("fail")
            raise Http404

    def get(self, request, pk, format=None):
        #print(pk)
        source = self.get_object(pk+" ")
        ser = SourceSerializer(source)
        return Response(ser.data)
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def test(request):
    return render(request, 'api/testpage.html');

'''class VisitList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['GET', 'POST'])
def visit_list(request, format=None):
    
    if request.method == 'GET':
        visits = Visit.objects.all()
        serializer = VisitSerializer(visits, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VisitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    '''