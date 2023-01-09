from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import *
from Main.serializers import *
from rest_framework import response,status,permissions,views
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.conf import settings

from .jwt import JWTAuthentication
# Create your views here.

class RegisterAPIView(views.APIView):

    authentication_classes=[]

    def post(self,request):
        # Saving the user
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        # Creating a user profile
        user = User.objects.get(email=request.data['email'])
        data={'user':user.id,'name':user.name,'email':user.email,'followers':[],'following':[]}
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

        return response.Response(serializer.data,status=status.HTTP_201_CREATED)



        

class LoginAPIView(GenericAPIView):
    authentication_classes=[]
    serializer_class=UserSerializer

    def post(self,request):
        email=request.data.get('email',None)
        password=request.data.get('password',None)
        user=User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token=jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256')

        res=response.Response()

        res.set_cookie(key='Token',value=token,httponly=True)
        res.data={  
            'Token':token
        }
        res.status_code=status.HTTP_200_OK
        return res


class LogoutAPIView(GenericAPIView):

    def post(self,request):
        res=response.Response()
        res.delete_cookie('Token')
        res.data={
            'message':'Success'
        }
        res.status_code=status.HTTP_200_OK
        return res        

