from django.shortcuts import render
from rest_framework import response,permissions,generics,status
from rest_framework.views import APIView
from .models import *
from .serializers import *

# Create your views here.


class UserProfileApiView(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    
    def get(self,request):
        user = request.user
        if UserProfile.objects.filter(user=user).exists():
            userprofile = UserProfile.objects.get(user=user)
            name=userprofile.name
            followers=len(list(userprofile.followers.all()))
            following=len(list(userprofile.following.all()))
            return response.Response({'name':name,'followers':followers,'following':following},status=status.HTTP_200_OK)
        else:
            return response.Response({'message':'User Profile does not exists'},status=status.HTTP_404_NOT_FOUND)


class FollowApiView(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    lookup_field=('id')

    def post(self,request,*args, **kwargs):
        uid = self.kwargs.get(self.lookup_field)
        user = request.user
      
        if User.objects.filter(id=uid).exists():
            follow=User.objects.get(id=uid)
            if user==follow:
                return response.Response({'message':'Cannot follow yourself'},status=status.HTTP_403_FORBIDDEN)

            elif UserProfile.objects.get(user=user).following.filter(id=uid).exists():
                        return response.Response({'message':'Already following'},status=status.HTTP_403_FORBIDDEN)
            else:
                UserProfile.objects.get(user=user).following.add(follow)
                UserProfile.objects.get(user=follow).followers.add(user)
                return response.Response({'message':'Followed'},status=status.HTTP_200_OK)
        else:
            return response.Response({'message':'User to be followed not found'},status=status.HTTP_404_NOT_FOUND)

class UnfollowApiView(APIView):
    parser_classes=(permissions.IsAuthenticated,)
    lookup_field=('id')

    def post(self,request,*args, **kwargs):
        uid=self.kwargs.get(self.lookup_field)
        user=request.user

        if User.objects.filter(id=uid).exists():
            unfollow=User.objects.get(id=uid)
            if user==unfollow:
                return response.Response({'message':'Cannot unfollow yourself'},status=status.HTTP_403_FORBIDDEN)
            
            elif UserProfile.objects.get(user=user).following.filter(id=uid).exists():
                UserProfile.objects.get(user=user).following.remove(unfollow)
                UserProfile.objects.get(user=unfollow).followers.remove(user)
                return response.Response({'message':'Unfollowed'},status=status.HTTP_200_OK)
            else:
                return response.Response({'message':'Not following'},status=status.HTTP_403_FORBIDDEN)


class PostApiView(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    
    def post(self,request):
        user=request.user
        try:
            title=request.data.get('title')
            description=request.data.get('description')
            post=Post.objects.create(user=user,title=title,description=description,comment=[])
            return response.Response({'Post-ID':post.id,'Title':post.title,'Description':post.description,'Created At':post.created_at},status=status.HTTP_201_CREATED)
        except:
            return response.Response({'message':'Invalid Data, both Title and Description are required'},status=status.HTTP_400_BAD_REQUEST)

            
class PostDetailApiView(generics.RetrieveDestroyAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    lookup_field=('id')

class AllPostApiView(APIView):
    permission_classes=(permissions.IsAuthenticated,)

    def get(self,request):
        user=request.user
        posts=Post.objects.filter(user=user).order_by('-created_at')
        serializer=PostSerializer(posts,many=True)
        return response.Response(serializer.data,status=status.HTTP_200_OK)


class LikeApiView(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    lookup_field=('id')

    def post(self,request,*args, **kwargs):
        pid=self.kwargs.get(self.lookup_field)
        user=UserProfile.objects.filter(user=request.user).first()

        if Post.objects.filter(id=pid).exists():
            post=Post.objects.filter(id=pid)
            if post.first() in user.posts_like.all():
                return response.Response({'message':'Post Already Liked'},status=status.HTTP_200_OK)
            else:
                user.posts_like.add(post.first())
               
                like=list(post.values('like'))[0]['like']
                
                post.update(like=like+1)
                return response.Response({'message':'Liked'},status=status.HTTP_200_OK)
        else:
            return response.Response({'message':'Post not found'},status=status.HTTP_404_NOT_FOUND)


class UnlikeApiView(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    lookup_field=('id')

    def post(self,request,*args, **kwargs):
        pid=self.kwargs.get(self.lookup_field)
        user=UserProfile.objects.filter(user=request.user).first()

        if Post.objects.filter(id=pid).exists():
            post=Post.objects.filter(id=pid)
            
            if post.first() in user.posts_like.all():
                user.posts_like.remove(post.first())
                like=list(post.values('like'))[0]['like']
                post.update(like=like-1)
                return response.Response({'message':'Unliked'},status=status.HTTP_200_OK)
            else:
                return response.Response({'message':'Post not liked'},status=status.HTTP_200_OK)
        else:
            return response.Response({'message':'Post not found'},status=status.HTTP_404_NOT_FOUND)


class CommentApiView(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    lookup_field=('id')

    def post(self,request,*args, **kwargs):
        pid=self.kwargs.get(self.lookup_field)
        user=request.user
        comment=request.data.get('comment')
        if Post.objects.filter(id=pid).exists():
            post=Post.objects.get(id=pid)
            post.comment.append({'user':user.email,'comment':comment})
            post.save()
            return response.Response(len(list(post.comment)),status=status.HTTP_201_CREATED)
        else:
            return response.Response({'message':'Post not found'},status=status.HTTP_404_NOT_FOUND)