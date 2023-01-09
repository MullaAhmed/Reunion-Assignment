from django.db import models

# Create your models here.

from Authentication.models import User

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,unique=True)
    followers=models.ManyToManyField(User,related_name='followers',blank=True)
    following=models.ManyToManyField(User,related_name='following',blank=True)
    posts_like=models.ManyToManyField('Post',related_name='posts_like',blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    description=models.TextField()

    like=models.IntegerField(default=0)
    comment=models.JSONField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title