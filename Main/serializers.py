from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id','user','name','email','followers','following']
    

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','user','title','description','like','comment','created_at']
