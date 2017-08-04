'''
Created on Jun 27, 2017

@author: Dan
'''
from rest_framework import serializers
from .models import Visit, Source
from django.contrib.auth.models import User

class VisitSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username');
    
    class Meta:
        model = Visit
        fields = ('user', 'domain', 'startTime', 'duration')
        
        
class SourceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Source
        fields = ('sitename', 'domain', 'bias')
        
#    domain = serializers.CharField(max_length=200);
#   startTime = serializers.DateTimeField();
#    duration = serializers.FloatField();

    #def create(self, validated_data):
    #    return Visit.objects.create(**validated_data)
    
    #def update(self, instance, validated_data):
    #    instance.domain = validated_data.get('domain', instance.domain)
    #    instance.startTime = validated_data.get('startTime', instance.startTime)
   #     instance.duration = validated_data.get('duration', instance.duration)
   #     return instance
   
class UserSerializer(serializers.ModelSerializer):
    #visits = serializers.PrimaryKeyRelatedField(many=True, 
     #                                           queryset=Visit.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'visits')