from django.shortcuts import render, redirect
from .models import Members
from user.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers


@api_view(['POST'])
def addMember(request):
    try:
        data = request.data
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        email = data.get('userEmail')
        user = User.objects.get(email=email)
        organisation = user.organisation
        created_by = user
        create_member = Members(name=name, age=age,gender=gender,created_by=created_by, organisation=organisation)
        create_member.save()
        return Response({'message': "user registered successfully"}, status=status.HTTP_200_OK)
    except KeyError as e:
        return Response({"message": "Data missing"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": "some error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def getMembers(request):
    try:
        data = request.data
        organisation = data.get('organisation')
        print(organisation)
        members = Members.objects.filter(organisation=organisation)
        print(members)
        return Response({'message': "fetched members successfully", "members":members.values()}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": "some error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

