from django.urls import path
from .views import * 
#import static 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('auth/signup/',Signup.as_view(),name='signup'),
    path('auth/signin/',Login.as_view(),name='login'),
    path('profile/',UserView.as_view(),name='user'),
    path('signout/',Logout.as_view(),name='logout'), 
    path('upload/',ProfileView.as_view(),name='upload'),

]


urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)   

