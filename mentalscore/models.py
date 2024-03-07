from django.db import models
from user.models import User
from members.models import Members


class MentalScore(models.Model):
    
    member = models.ForeignKey(Members, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, default='')
    score = models.FloatField() 
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return  self.name