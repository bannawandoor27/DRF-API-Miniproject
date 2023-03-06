from django.conf import settings
from django.shortcuts import render
#import response from drf
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


from rest_framework import status
from .serializers import UserSerializer,UserImageSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser


def check_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is None:
        raise AuthenticationFailed('User is not logged in')
    try:
        payload = jwt.decode(token,'secret_key', algorithms=['HS256'])
    except jwt.DecodeError:
        return Response({'error':'Decode error'},status=status.HTTP_401_UNAUTHORIZED)
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Invalid token')
    return payload


class Signup(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

secret = settings.SECRET_KEY
class Login(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email)
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed('User does not exist')

        if not user.check_password(password):
            raise AuthenticationFailed('Password is incorrect')
        
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),


        }
        token = jwt.encode(payload,'secret_key', algorithm='HS256')

        response = Response()
        response.data = {
                            'user_id': user.id,
                            'email': user.email,
                            'token': token,
                            'username':user.username,
                            'mobile':user.mobile_number,
                            'date_of_birth':user.date_of_birth,
                            'is_superuser': user.is_superuser

                        }


        return response

class UserView(APIView):
    def get(self,request):
        payload = check_token(request)
        user = User.objects.filter(id=payload['user_id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
        
class ProfileImageView(APIView):
    def put(self, request, format=None):
        payload = check_token(request)
        user = User.objects.filter(id=payload['user_id']).first()
        serializer = UserImageSerializer(data=request.data ,instance=user)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


