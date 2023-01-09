from re import I
from django.urls import path
from .views import *
urlpatterns = [
    path('user/',UserProfileApiView.as_view(),name='user'),
    path('follow/<int:id>/',FollowApiView.as_view(),name='follow'),
    path('unfollow/<int:id>/',UnfollowApiView.as_view(),name='unfollow'),
    path('post/',PostApiView.as_view(),name='post'),
    path('post/<int:id>/',PostDetailApiView.as_view(),name='post_detail'),
    path('all_posts/',AllPostApiView.as_view(),name='all_posts'),
    path('like/<int:id>/',LikeApiView.as_view(),name='like'),
    path('unlike/<int:id>/',UnlikeApiView.as_view(),name='unlike'),
    path('comment/<int:id>/',CommentApiView.as_view(),name='comment'),
]
