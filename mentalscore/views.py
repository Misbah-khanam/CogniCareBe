from django.shortcuts import render, redirect
from .models import Members
from user.models import User
from mentalscore.models import MentalScore
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from .calculater import calculater
from googletrans import Translator


@api_view(['POST'])
def calculateScore(request):
    try:
        data = request.data
        member = data.get("member")
        memobj = Members.objects.get(id = member.get("id"))
        answers = data.get("answers")
        trans_answers = []

        for ans in answers:
            translator = Translator()
            detected = translator.detect(ans)
            translation = translator.translate(ans, dest="en")
            print(f"Translated Text: {translation.text}")
            trans_answers.append(translation.text)

        email = data.get('userEmail')
        user = User.objects.get(email=email)
        print(answers)
        print(trans_answers)
        score = calculater(trans_answers)
        mentalscore = MentalScore(member=memobj,score=score,name=member.get("name"),created_by=user)
        mentalscore.save()
        return Response({'message': "calculated successfully", "score" :score}, status=status.HTTP_200_OK)
    except KeyError as e:
        return Response({"message": "Data missing"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": "some error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def getAllScoresOrg(request):
    try:
        data = request.data
        organisation = data.get("organisation")
        allScores = MentalScore.objects.filter(member__organisation=organisation)
        return Response({'message': "fetched successfully", "scores" : allScores.values()}, status=status.HTTP_200_OK)
    except KeyError as e:
        return Response({"message": "Data missing"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": "some error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def getMemberScores(request):
    try:
        data = request.data
        member_name = data.get("member_name")
        MemberScores = MentalScore.objects.filter(member__name=member_name)
        return Response({'message': "fetched successfully", "MemberScores" : MemberScores.values()}, status=status.HTTP_200_OK)
    except KeyError as e:
        return Response({"message": "Data missing"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": "some error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def detect_and_translate(request):
    data = request.data
    text = data.get("text")
    target = data.get("target")
    translator = Translator()
    detected = translator.detect(text)
    print(f"Detected Language: {detected.lang}")
    print(target)
    translation = translator.translate(text, dest=target)
    print(f"Translated Text: {translation.text}")
    return Response({'message': "fetched successfully", "translated" : translation.text }, status=status.HTTP_200_OK)