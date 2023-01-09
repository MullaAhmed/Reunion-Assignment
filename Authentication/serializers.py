from sre_constants import MAX_UNTIL
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,min_length=6,write_only=True
    )

    class Meta:
        model=User
        fields=['id','name','email','password']

    def create(self, validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance # Hashes the password

