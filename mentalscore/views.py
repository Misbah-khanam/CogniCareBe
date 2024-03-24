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
from .utils import predict_emotion
from cognicarebe.settings import BASE_DIR
from pathlib import Path
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


@api_view(['POST'])
def calculateScore(request):
    # try:
        data = request.data
        member_id = data.get("member_id")
        member_name = data.get("member_name")
        memobj = Members.objects.get(id = member_id)
        answers = data.get("answers").split(',')
        trans_answers = []

        for ans in answers:
            translator = Translator()
            detected = translator.detect(ans)
            translation = translator.translate(ans, dest="en")
            print(f"Translated Text: {translation.text}")
            trans_answers.append(translation.text)

        email = data.get('userEmail')
        user = User.objects.get(email=email)

        text_score = calculater(trans_answers)
        image_score = predict_emotion_view(request)
        score = calculate_overall_score(text_score,image_score)

        print(text_score)
        print(image_score)

        mentalscore = MentalScore(member=memobj,score=score,name=member_name,created_by=user)
        mentalscore.save()
        return Response({'message': "calculated successfully", "score" :score}, status=status.HTTP_200_OK)
    # except KeyError as e:
    #     return Response({"message": "Data missing"}, status=status.HTTP_400_BAD_REQUEST)
    # except Exception as e:
    #     return Response({"message": "some error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

def calculate_overall_img_score(emotions):
    sad_count = emotions.count('fear') + emotions.count('sad') + emotions.count('angry')
    happy_count = len(emotions) - sad_count
    raw_score = (happy_count - sad_count) / len(emotions)

    # Normalize the score to be between 0 and 1
    min_score = -1 # Assuming the worst possible score is -1 (all sad emotions)
    max_score = 1 # Assuming the best possible score is 1 (all happy emotions)
    normalized_score = (raw_score - min_score) / (max_score - min_score)

    scaled_score = normalized_score * 50

    return scaled_score

def predict_emotion_view(request):
    image_paths = []
    if 'images[]' not in request.FILES:
        return Response({'error': 'No image files in request'}, status=status.HTTP_400_BAD_REQUEST)
    images = request.FILES.getlist('images[]')
    image_directory = Path(settings.MEDIA_ROOT)

    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    for image in images:
        filename = fs.save(os.path.join(image_directory.as_posix(), image.name), image)
        image_path = image_directory / filename
        image_paths.append(image_path)

    emotions = [predict_emotion(path) for path in image_paths]
    score = calculate_overall_img_score(emotions)

    return score



def calculate_overall_score(text_score, image_score, text_weight=0.5, image_weight=0.5):
    overall_score = text_weight * text_score + image_weight * image_score
    return overall_score