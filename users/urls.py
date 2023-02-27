from django.urls import path
from .views import * 
#import static 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('signup/',Signup.as_view(),name='signup'),
    path('login/',Login.as_view(),name='login'),
    path('user/',UserView.as_view(),name='user'),
    path('logout/',Logout.as_view(),name='logout'),

]


urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)   

