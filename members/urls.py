from django.urls import path
from .views import addMember, getMembers

urlpatterns = [
    path("add-member/",addMember, name="addMember"),
    path("get-member/",getMembers, name="getMembers"),
]