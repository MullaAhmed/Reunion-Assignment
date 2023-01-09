from re import I
from django.urls import path
from Authentication import views 
urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(),name="Register"), # Creates Users
    path('authenticate/', views.LoginAPIView.as_view(),name="Login"), # Creates tokens
    path('logout/', views.LogoutAPIView.as_view(),name="Logout"), # Deletes token
]
