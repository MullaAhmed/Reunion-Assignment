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

        follow=self.client.post(reverse("follow",kwargs={"id":2}))
        resp=self.client.get(reverse("user"))

        self.assertEqual(follow.status_code,status.HTTP_200_OK)
        self.assertEqual(resp.data['following'],1)
        self.assertEqual(len(list(UserProfile.objects.filter(id=2).first().followers.all())),1)

    
    def test_unfollow_user_check(self):
        self.authenticate(name="test",email="test@gmail.com",password="test@123")
        self.dummy_user(name="unfollow",email="unfollow@gmail.com",password="test@123")

        follow=self.client.post(reverse("follow",kwargs={"id":2}))
        resp=self.client.get(reverse("user"))

        self.assertEqual(follow.status_code,status.HTTP_200_OK)
        self.assertEqual(resp.data['following'],1)
        self.assertEqual(len(list(UserProfile.objects.filter(id=2).first().followers.all())),1)

        unfollow=self.client.post(reverse("unfollow",kwargs={"id":2}))
        resp=self.client.get(reverse("user"))

        self.assertEqual(unfollow.status_code,status.HTTP_200_OK)
        self.assertEqual(resp.data['following'],0)
        self.assertEqual(len(list(UserProfile.objects.filter(id=2).first().followers.all())),0)

    def test_create_post(self):
        self.authenticate(name="test",email="test@gmail.com",password="test@123")
        resp=self.client.post(reverse("post"),{"title":"Test Post 1","description":"This is post 1 by user 1"})
        self.assertEqual(resp.status_code,status.HTTP_201_CREATED)
    
    def test_delete_post(self):
        self.authenticate(name="test",email="test@gmail.com",password="test@123")
        resp=self.client.post(reverse("post"),{"title":"Test Post 1","description":"This is post 1 by user 1"})
        self.assertEqual(resp.status_code,status.HTTP_201_CREATED)

        resp=self.client.delete(reverse("post_detail",kwargs={"id":1}))
        self.assertEqual(resp.status_code,status.HTTP_204_NO_CONTENT)

    def test_comment(self):
        self.authenticate(name="test",email="test@gmail.com",password="test@123")
        resp=self.client.post(reverse("post"),{"title":"Test Post 1","description":"This is post 1 by user 1"})
        self.assertEqual(resp.status_code,status.HTTP_201_CREATED)

        resp=self.client.post(reverse("comment",kwargs={"id":1}),{"comment":"This is comment 1"})
        self.assertEqual(resp.status_code,status.HTTP_201_CREATED)
    
    def test_user_authentication_with_a_field_missing(self):
        user=User.objects.create_user(name="test",email="test@gmail.com",password="test@123")
        resp=self.client.post(reverse('Login'),{"password": "test@123"})
        self.assertEqual(resp.status_code,status.HTTP_403_FORBIDDEN)

    def test_create_post_with_a_field_missing(self):
        self.authenticate(name="test",email="test@gmail.com",password="test@123")
        resp=self.client.post(reverse("post"),{"description":"This is post 1 by user 1"})
        self.assertEqual(resp.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_get_single_post_with_wrong_id(self):
        self.authenticate(name="test",email="test@gmail.com",password="test@123")
        resp=self.client.post(reverse("post"),{"title":"Test Post 1","description":"This is post 1 by user 1"})
        self.assertEqual(resp.status_code,status.HTTP_201_CREATED)
    
        resp=self.client.get(reverse("post_detail",kwargs={"id":2}))
        self.assertEqual(resp.status_code,status.HTTP_404_NOT_FOUND)

    def test_delete_post_with_a_field_missing(self):
        self.authenticate(name="test",email="test@gmail.com",password="test@123")
        resp=self.client.post(reverse("post"),{"title":"Test Post 1","description":"This is post 1 by user 1"})
        self.assertEqual(resp.status_code,status.HTTP_201_CREATED)

        resp=self.client.delete(reverse("post_detail",kwargs={"id":2}))
        self.assertEqual(resp.status_code,status.HTTP_404_NOT_FOUND)

    def test_comment_with_a_field_missing(self):
        self.authenticate(name="test",email="test@gmail.com",password="test@123")
        resp=self.client.post(reverse("post"),{"title":"Test Post 1","description":"This is post 1 by user 1"})
        self.assertEqual(resp.status_code,status.HTTP_201_CREATED)

        resp=self.client.post(reverse("comment",kwargs={"id":2}),{"comment":"This is comment 1"})
        self.assertEqual(resp.status_code,status.HTTP_404_NOT_FOUND)
    