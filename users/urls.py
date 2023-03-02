from django.urls import path
from .views import * 
#import static 

urlpatterns = [
    path('auth/signup/',Signup.as_view(),name='signup'),
    path('auth/signin/',Login.as_view(),name='login'),
    path('profile/',UserView.as_view(),name='user'),
    path('signout/',Logout.as_view(),name='logout'), 
    path('upload/',ProfileView.as_view(),name='upload'),

]



