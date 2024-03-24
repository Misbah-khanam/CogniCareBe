from django.urls import path
from .views import calculateScore, getAllScoresOrg, getMemberScores,detect_and_translate, predict_emotion_view

urlpatterns = [
    path("calculate-score/",calculateScore, name="calculateScore"),
    path("get-all-score/",getAllScoresOrg, name="getAllScoresOrg"),
    path("get-member-score/",getMemberScores, name="getMemberScores"),
    path("translate/",detect_and_translate, name="translate"),
    path('predict_emotion/', predict_emotion_view, name='predict_emotion')
]