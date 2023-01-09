from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from Authentication.models import User
from .models import *
from .serializers import *
# Create your tests here.

class Tests(APITestCase):

    def dummy_user(self,name,email,password):
        user=User.objects.create_user(name=name,email=email,password=password)
       
        data={'user':user.id,'name':user.name,'email':user.email,'followers':[],'following':[]}
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

    def authenticate(self,name,email,password):
        self.dummy_user(name,email,password)
        resp=self.client.post(reverse('Login'),{"email": email, "password": password})

        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+str(resp.data["Token"]))
        

    def test_user_authentication(self):
        user=User.objects.create_user(name="test",email="test@gmail.com",password="test@123")
        resp=self.client.post(reverse('Login'),{"email": "test@gmail.com", "password": "test@123"})
        self.assertEqual(resp.status_code,status.HTTP_200_OK)

    def test_get_user_profile(self):
        self.authenticate(name="test",email="test@gmail.com",password="test@123")
        resp=self.client.get(reverse("user"))
        self.assertEqual(resp.status_code,status.HTTP_200_OK)

    def test_follow_user_check(self):
        self.authenticate(name="test",email="test@gmail.com",password="test@123")
        self.dummy_user(name="follow",email="follow@gmail.com",password="test@123")

        print(UserProfile.objects.filter().all()[1])


        follow=self.client.post(reverse("follow",kwargs={"id":2}))
        resp=self.client.get(reverse("user"))

        self.assertEqual(follow.status_code,status.HTTP_200_OK)
        self.assertEqual(resp.data['following'],1)
        self.assertEqual(len(list(UserProfile.objects.filter(id=2).first().followers.all())),1)

    
    def test_unfollow_user_check(self):
        self.authenticate(name="test",email="test@gmail.com",password="test@123")
        self.dummy_user(name="unfollow",email="unfollow@gmail.com",password="test@123")

        print(UserProfile.objects.filter().all())

        follow=self.client.post(reverse("follow",kwargs={"id":2}))
        resp=self.client.get(reverse("user"))

        print(follow.data)

        self.assertEqual(follow.status_code,status.HTTP_200_OK)
        self.assertEqual(resp.data['following'],1)
        self.assertEqual(len(list(UserProfile.objects.filter(id=2).first().followers.all())),1)

        unfollow=self.client.post(reverse("unfollow",kwargs={"id":2}))
        resp=self.client.get(reverse("user"))

        self.assertEqual(unfollow.status_code,status.HTTP_200_OK)
        self.assertEqual(resp.data['following'],0)
        self.assertEqual(len(list(UserProfile.objects.filter(id=2).first().followers.all())),0)


    
    