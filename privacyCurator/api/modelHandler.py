'''
Created on Jul 4, 2017

@author: Dan
'''
from .models import Visit
from api.serializers import VisitSerializer

def addOrUpdateVisit(serializer):
    thisDomain = serializer.validated_data["domain"]
    thisStartTime = serializer.validated_data["startTime"]
    thisDuration = serializer.validated_data["duration"]

    print(thisDomain+": "+str(thisDuration)+" seconds @ "+str(thisStartTime));
    
    if (Visit.objects.filter(domain=thisDomain)):
        visit = Visit.objects.get(domain=thisDomain)
        visit.duration += thisDuration
        visit.save()
    else:
        serializer.save()
        