from django.shortcuts import render, redirect
from user.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers


@api_view(['POST'])
def register_user(request):
    try:
        data = request.data
        print(data)
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        password = make_password(f"{data.get('password')}")
        userType = data.get('userType')
        organisation = data.get('organisation')
        create_user = User(name=name, email=email, phone=phone, user_type=userType, password=password, organisation=organisation)
        create_user.save()
        print(name, email, phone, password, userType,organisation)
        return Response({'messages': "user registered successfully"}, status=status.HTTP_200_OK)
    except KeyError as e:
        return Response({"message": "Data missing"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": "some error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   

@api_view(['POST'])
def login_user(request):
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()
        if(user):
            user_authenticate = authenticate(request, email=email, password=password)
            if(user_authenticate):
                login(request, user_authenticate)
                return Response({"message": "login successfull", "user":serializers.serialize("json",[user])}, status=status.HTTP_200_OK)  
            else:
                return Response({"message": "password does not match"}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({"message": "user does not exist"}, status=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
        return Response({"message": "some error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def logout_view(request):
    try:
        logout(request)
        return Response({"message":"user loogged out"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": "some error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

