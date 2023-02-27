from django.conf import settings
from django.shortcuts import render
#import response from drf
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime



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

        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed('User does not exist')

        if not user.check_password(password):
            raise AuthenticationFailed('Password is incorrect')
        
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow()

        }
        token = jwt.encode(payload,'secret', algorithm='HS256').decode('utf-8')


        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
                            'user_id': user.id,
                            'email': user.email,
                            'name': user.name,
                            'token': token
                        }


        return response

class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if token is None:
            raise AuthenticationFailed('User is not logged in')
        try:
            payload = jwt.decode(token,'secret', algorithm=['HS256'])
        except jwt.DecodeError:
            return Response({'error':'Decode error'},status=status.HTTP_401_UNAUTHORIZED)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token')
        user = User.objects.filter(id=payload['user_id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

        
class Logout(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
                'message': 'Logged out successfully'
        }
        return response
        
